# Doc QA Bot

LangChain, ChromaDB, Ollama 기반의 로컬 RAG(Retrieval Augmented Generation) Q&A 봇.
LangChain / LangGraph 공식 문서를 지식 베이스로 삼아 개발 관련 질문에 답변한다.

## 스택

| 역할 | 기술 |
|---|---|
| LLM | Ollama (`qwen2.5:7b`) |
| 임베딩 | Ollama (`nomic-embed-text`, 768차원) |
| 벡터 DB | ChromaDB (로컬 파일 저장) |
| 프레임워크 | LangChain |
| API | FastAPI |
| 컨테이너 | Docker Compose |

## RAG 파이프라인

```
[문서] → loader → splitter → embedder → ChromaDB
                                              ↕
[질문] → embedder → retriever → chain(LLM) → [답변]
```

## 프로젝트 구조

```
doc-qa-bot/
├── app/
│   ├── main.py                  # FastAPI 엔트리포인트
│   ├── api/
│   │   ├── deps.py              # 의존성 주입 (lru_cache 싱글턴)
│   │   ├── schemas.py           # 요청/응답 Pydantic 모델
│   │   └── routers/
│   │       ├── health.py        # GET /health
│   │       ├── query.py         # POST /query
│   │       └── ingest.py        # POST /ingest
│   ├── service/
│   │   ├── query_service.py     # 질문 → 체인 호출
│   │   └── ingest_service.py    # 문서 로드 → 분할 → 저장
│   ├── domain/
│   │   ├── ingestion/
│   │   │   ├── loader.py        # DirectoryLoader (md/txt/pdf)
│   │   │   └── splitter.py      # RecursiveCharacterTextSplitter
│   │   ├── retrieval/
│   │   │   └── retriever.py     # VectorStore → Retriever 변환
│   │   └── llm/
│   │       ├── ollama_client.py # OllamaLLM 팩토리
│   │       └── chain.py         # LCEL RAG 체인
│   └── infrastructure/
│       ├── embedder.py          # OllamaEmbeddings 팩토리
│       └── vectorstore.py       # ChromaDB 팩토리
├── config/
│   └── settings.py              # pydantic-settings (.env 오버라이드)
├── data/
│   ├── raw/                     # 수집된 문서 (langchain/, langgraph/)
│   └── processed/chroma/        # ChromaDB 저장소
├── scripts/
│   └── scrape_docs.py           # docs.langchain.com 스크래핑
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── tests/
│   └── test_chain.py
├── .env
└── requirements.txt
```

## 시작하기

### 1. Ollama 및 API 서버 실행

```bash
cd docker
docker compose up -d
```

### 2. 모델 확인

```bash
curl http://localhost:11434/api/tags
```

`qwen2.5:7b`, `nomic-embed-text` 두 모델이 있어야 한다.
없으면 컨테이너 안에서 pull:

```bash
docker exec -it ollama ollama pull qwen2.5:7b
docker exec -it ollama ollama pull nomic-embed-text
```

### 3. 문서 수집

```bash
python scripts/scrape_docs.py
```

`data/raw/langchain/`, `data/raw/langgraph/` 에 마크다운 파일이 저장된다.

### 4. 문서 인제스트 (벡터화 및 저장)

```bash
curl -X POST http://localhost:8000/ingest
```

### 5. 질문하기

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "LangChain이 뭐야?"}'
```

## 환경 변수 (.env)

| 변수 | 기본값 | 설명 |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama 서버 주소 |
| `LLM_MODEL` | `qwen2.5:7b` | 사용할 LLM 모델 |
| `LLM_TEMPERATURE` | `0.0` | 생성 온도 |
| `EMBEDDING_MODEL` | `nomic-embed-text` | 임베딩 모델 |
| `CHROMA_PERSIST_DIR` | `data/processed/chroma` | ChromaDB 저장 경로 |
| `CHROMA_COLLECTION` | `docs` | 컬렉션 이름 |
| `DATA_RAW_DIR` | `data/raw` | 원본 문서 경로 |
| `CHUNK_SIZE` | `1000` | 청크 최대 길이 |
| `CHUNK_OVERLAP` | `200` | 청크 간 겹치는 길이 |
| `RETRIEVER_K` | `4` | 검색할 청크 수 |

## 테스트

```bash
# 통합 테스트 (Ollama 실행 필요)
.venv/Scripts/python -m pytest tests/ -v
```
