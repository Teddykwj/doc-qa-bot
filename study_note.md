# Doc QA Bot 개발 스터디 노트

## 프로젝트 스택
- LLM: Ollama (qwen2.5:7b)
- 임베딩: nomic-embed-text (768차원)
- 벡터 DB: ChromaDB (로컬)
- 프레임워크: LangChain
- API: FastAPI

---

## RAG 파이프라인 흐름

```
[문서] → loader → splitter → embedder → ChromaDB
                                              ↕
[질문] → embedder → retriever → chain(LLM) → [답변]
```

---

## 1. 데이터 수집

### 수집 방법
- GitHub sparse checkout 시도 → 실패 (docs가 레포에 없음)
- docs.langchain.com 웹 스크래핑으로 전환
- sitemap.xml에서 URL 목록 수집 → HTML 스크래핑 → 마크다운 변환

### 수집 결과
- langchain: 61개 파일
- langgraph: 30개 파일
- 저장 위치: `data/raw/`

---

## 2. Loader

파일: `app/domain/ingestion/loader.py`

### 개념
- 문서 파일을 읽어서 LangChain `Document` 객체 리스트로 반환
- `Document` = `page_content`(텍스트) + `metadata`(출처 파일경로 등)
- 파일 포맷마다 다른 Loader 클래스를 사용

### LangChain Document Loader 종류
| 클래스 | 대상 |
|--------|------|
| `UnstructuredMarkdownLoader` | `.md` 파일 |
| `TextLoader` | `.txt` 파일 |
| `PyPDFLoader` | `.pdf` 파일 |
| `DirectoryLoader` | 디렉토리 전체를 glob 패턴으로 탐색 |

### DirectoryLoader 동작 방식
```
DirectoryLoader(source_dir, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
```
- `glob="**/*.md"` → 하위 디렉토리 포함 모든 `.md` 파일 탐색
- `loader_cls` → 파일 하나당 어떤 Loader로 읽을지 지정
- `silent_errors=True` → 읽기 실패한 파일은 건너뜀 (중단 없이 진행)

### 코드 흐름
```python
def load_documents(source_dir: str) -> List[Document]:
    loaders = {
        "**/*.md": UnstructuredMarkdownLoader,
        "**/*.txt": TextLoader,
        "**/*.pdf": PyPDFLoader,
    }
    docs = []
    for glob_pattern, loader_cls in loaders.items():
        # 포맷별로 DirectoryLoader를 만들어 순서대로 수집
        loader = DirectoryLoader(..., glob=glob_pattern, loader_cls=loader_cls)
        docs.extend(loader.load())  # List[Document] 누적
    return docs
```

### 반환 결과
```python
Document(
    page_content="LangChain is a framework ...",
    metadata={"source": "data/raw/langchain/overview.md"}
)
```

---

## 3. Splitter (청킹)

파일: `app/domain/ingestion/splitter.py`

### 개념
- LLM의 컨텍스트 길이 제한 때문에 문서를 작은 조각(chunk)으로 분할
- chunk_size: 청크 하나의 최대 글자 수
- chunk_overlap: 앞뒤 청크가 겹치는 글자 수 (문맥 유지)

### 왜 overlap이 필요한가?
- 문장이 청크 경계에서 잘리면 의미가 손실될 수 있음
- overlap으로 인접 청크 간 문맥 연결을 유지

### RecursiveCharacterTextSplitter

LangChain의 범용 텍스트 분할기. 구분자를 우선순위 순서대로 시도해서 청크를 자름.

**구분자 우선순위 (기본값)**
```
"\n\n"  →  "\n"  →  " "  →  ""
```
1. 문단 단위로 먼저 자르려 시도
2. 문단으로 안 되면 줄 단위
3. 줄로도 안 되면 단어 단위
4. 그래도 크면 글자 단위로 강제 분할

→ 가능한 한 의미 단위(문단 > 줄 > 단어)를 유지하려는 전략

**구분자 선택 기준: chunk_size**

각 구분자로 쪼갠 조각이 chunk_size 이하인지 확인하고, 초과하면 다음 구분자로 넘어감.

```
chunk_size=100 일 때

문단A (50자)  → ✅ 100자 이하 → 청크로 사용
문단B (80자)  → ✅ 100자 이하 → 청크로 사용
문단C (150자) → ❌ 100자 초과 → \n 으로 재시도
  줄1 (90자)  → ✅ 100자 이하 → 청크로 사용
  줄2 (60자)  → ✅ 100자 이하 → 청크로 사용
```

→ "최대한 의미 있는 단위로 자르되, chunk_size를 절대 넘지 않는다"

**동작 예시**
```
chunk_size=100, chunk_overlap=20 일 때

원문:  [----100자----][----100자----][----100자----]
청크:  [  chunk1  ]
                [  chunk2  ]       ← 20자 겹침
                           [  chunk3  ]
```

**파라미터**
| 파라미터 | 설명 | 현재 설정 |
|----------|------|-----------|
| `chunk_size` | 청크 최대 길이 (문자 수) | 1000 |
| `chunk_overlap` | 인접 청크 간 겹치는 길이 | 200 |

**코드**
```python
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
# List[Document] → 더 잘게 나뉜 List[Document]
# metadata는 원본 Document에서 그대로 상속됨
```

---

## 4. Embedder

파일: `src/ingestion/embedder.py`

### 개념
- 텍스트를 고정 길이의 숫자 벡터로 변환
- 의미가 비슷한 텍스트 → 벡터 공간에서 가까운 위치
- 모델: nomic-embed-text (768차원)

### 코드 메모

```python
# 학습 내용 기록
```

---

## 5. VectorStore (ChromaDB)

파일: `app/infrastructure/vectorstore.py`

### 개념
- 벡터(숫자 배열)를 저장하고, 질문 벡터와 가장 유사한 벡터를 빠르게 찾아주는 DB
- embedder는 텍스트 → 벡터 변환만 담당, 저장/검색은 VectorStore가 담당

### 유사도 계산: 코사인 유사도
- 두 벡터 사이의 각도로 유사성 측정 (1에 가까울수록 유사)
- 전체 비교 대신 HNSW 인덱스로 빠른 근사 탐색

### LangChain VectorStore 주요 메서드
| 메서드 | 설명 |
|---|---|
| `add_documents(docs)` | `List[Document]` 저장 (벡터화 자동) |
| `add_texts(texts)` | 문자열 리스트로 직접 저장 |
| `similarity_search(query, k=4)` | 유사한 Document k개 반환 |
| `similarity_search_with_score(query)` | Document + 유사도 점수 반환 |
| `max_marginal_relevance_search(query)` | 유사도 + 다양성 동시 고려 (MMR) |
| `as_retriever(**kwargs)` | LCEL 체인 연결용 Retriever 객체로 변환 |

### 구현체 비교
| 구현체 | 특징 |
|---|---|
| **ChromaDB** | 로컬 파일 저장, 메타데이터 필터 내장, 서버 불필요 |
| **FAISS** | 순수 인메모리, 대용량 고속 검색 |
| **Pinecone** | 클라우드 관리형, 프로덕션용 |
| **PGVector** | PostgreSQL 확장, 기존 DB에 벡터 추가 |

→ LangChain 인터페이스가 동일하므로 구현체를 바꿔도 Service 코드는 그대로 유지됨

### 코드
```python
def get_vectorstore(embeddings: Embeddings, collection_name: str | None = None) -> Chroma:
    return Chroma(
        collection_name=collection_name or settings.chroma_collection,
        embedding_function=embeddings,   # add_documents 시 내부에서 자동 호출
        persist_directory=settings.chroma_persist_dir,
    )
```

---

## 6. Retriever

파일: `src/retrieval/retriever.py`

### 개념
- VectorStore에서 질문과 관련된 청크를 가져오는 역할
- search_type: similarity(코사인 유사도), mmr(다양성 고려) 등
- k: 몇 개의 청크를 가져올지

### 코드 메모

```python
# 학습 내용 기록
```

---

## 7. RAG Chain

파일: `app/domain/llm/chain.py`

### 개념
- Retriever로 가져온 청크 + 원래 질문을 프롬프트에 조합
- LLM에게 "이 문서를 참고해서 답해" 라고 전달
- LangChain Expression Language (LCEL)로 체인 구성

### LCEL 파이프라인 문법

`|` 는 파이프 연산자. 왼쪽 출력이 오른쪽 입력으로 자동 전달됨.

```python
chain = {"context": retriever | format_docs, "question": RunnablePassthrough()}
      | RAG_PROMPT
      | llm
      | StrOutputParser()
```

실행 흐름:
```
invoke("LangChain이 뭐야?")
    ↓
┌─────────────────────────────────────┐
│ context: retriever | format_docs    │ → 문서 검색 → 문자열로 변환
│ question: RunnablePassthrough()     │ → 질문 그대로 통과
└─────────────────────────────────────┘
    ↓
RAG_PROMPT   → {context}, {question} 채워서 프롬프트 완성
    ↓
llm          → AIMessage(content="...") 반환
    ↓
StrOutputParser → .content 추출 → 문자열 반환
```

### 핵심 컴포넌트

**`retriever | format_docs`**
- `|` 로 연결 시 LangChain이 일반 함수를 `RunnableLambda`로 자동 래핑
- retriever: 질문 → `List[Document]`
- format_docs: `List[Document]` → 청크들을 `\n\n`으로 합친 문자열

**`RunnablePassthrough`**
- 입력을 변환 없이 그대로 출력하는 Runnable
- 딕셔너리 조합 시 원본 질문을 `question` 키로 유지하기 위해 사용
- 일반 문자열은 Runnable이 아니므로 체인에 연결 불가 → 이걸로 대체

**`StrOutputParser`**
- LLM이 반환하는 `AIMessage` 객체에서 `.content`(텍스트)만 추출
- 없으면 AIMessage 객체가 그대로 반환되어 문자열로 쓸 수 없음

### 코드
```python
RAG_PROMPT = ChatPromptTemplate.from_template("""...\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def build_rag_chain(retriever, llm):
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )
```

---

### Runnable

LangChain에서 `|` 로 연결하거나 `invoke`를 호출할 수 있는 모든 객체의 베이스 클래스.

**판단 기준**: `langchain_core.runnables.Runnable`을 상속받았는지
```python
from langchain_core.runnables import Runnable
isinstance(chain, Runnable)  # True / False
```

**상속 구조**
```
Runnable
├── RunnableLambda       ← 일반 함수를 Runnable로 래핑
├── RunnablePassthrough  ← 입력 그대로 통과
├── RunnableParallel     ← 여러 Runnable 병렬 실행
├── ChatPromptTemplate
├── BaseLLM / BaseChatModel
├── BaseRetriever
└── BaseOutputParser
```

**공통 메서드**
| 메서드 | 설명 |
|---|---|
| `invoke(input)` | 단일 입력 → 단일 출력 (동기) |
| `ainvoke(input)` | 비동기 버전 |
| `batch([...])` | 여러 입력 동시 처리 |
| `stream(input)` | 토큰 단위 스트리밍 출력 |

일반 함수는 Runnable이 아니지만 `|` 로 연결 시 LangChain이 자동으로 `RunnableLambda`로 래핑해줌.

### RunnableLambda

일반 함수를 Runnable로 만드는 래퍼. `invoke` 등 Runnable 인터페이스를 부여함.

```python
def _run(question: str) -> dict:
    ...

_run.invoke("질문")           # AttributeError — 일반 함수는 invoke 없음
RunnableLambda(_run).invoke("질문")  # 정상 동작
```

LCEL `|` 파이프만으로 표현하기 복잡한 로직(예: 출처 반환)을 일반 함수로 작성하고 래핑할 때 사용.

### Document 객체

LangChain에서 문서 청크를 표현하는 기본 단위.

```python
Document(
    page_content="LangChain is a framework...",  # 청크 텍스트
    metadata={"source": "data/raw/langchain/overview.md"}  # 출처 등 부가정보
)
```

- `doc.page_content` — 청크 텍스트. `format_docs`에서 프롬프트 context로 변환할 때 사용
- `doc.metadata.get("source", "")` — 출처 경로. `"source"` 키가 없을 때 `""` 반환 (KeyError 방지)

### 출처(sources) 추출 패턴

```python
sources = sorted({doc.metadata.get("source", "") for doc in docs})
```

- `{}` (set 컴프리헨션) — 같은 파일에서 여러 청크가 나와도 중복 제거
- `sorted()` — set은 순서 비보장이므로 알파벳순 정렬로 응답 일관성 확보

---

## 8. API (FastAPI)

파일: `src/api/`

### 구조
- `app.py`: 라우터 등록
- `deps.py`: 의존성 주입 (lru_cache로 싱글턴 관리)
- `schemas.py`: 요청/응답 모델
- `routers/`: 엔드포인트별 분리

### Depends 동작 방식
- `Depends(get_chain)`: 요청마다 get_chain() 호출
- `lru_cache`: 이미 만든 객체 재사용 (매 요청마다 Ollama 연결 안 맺음)
- `app.dependency_overrides`: 테스트 시 mock으로 교체 가능

### 코드 메모

```python
# 학습 내용 기록
```

---

## 9. 인제스트 중복 방지

파일: `app/service/ingest_service.py`

### 문제
`add_documents()`는 호출할 때마다 새 UUID를 생성해서 저장함.
같은 문서를 두 번 ingest하면 ChromaDB에 동일한 청크가 중복으로 쌓임.
→ 검색 결과에 같은 내용이 여러 번 등장, 벡터 공간 오염

### 해결 전략: 결정론적 ID + 중복 필터

```
청크 → ID 생성 (md5) → ChromaDB에 존재 여부 확인 → 없는 것만 저장
```

**ID 생성 방식**
```python
def _chunk_id(source: str, content: str) -> str:
    return hashlib.md5(f"{source}:{content}".encode()).hexdigest()
```
- `source`: 문서 파일 경로 (metadata에서 추출)
- `content`: 청크 텍스트
- 두 값이 같으면 항상 같은 ID → 멱등성 보장

**중복 필터링**
```python
ids = [_chunk_id(c.metadata.get("source", ""), c.page_content) for c in chunks]

existing = set(self._vectorstore._collection.get(ids=ids)["ids"])
new_pairs = [(chunk, id_) for chunk, id_ in zip(chunks, ids) if id_ not in existing]

if new_pairs:
    new_chunks, new_ids = zip(*new_pairs)
    self._vectorstore.add_documents(list(new_chunks), ids=list(new_ids))
```
- `_collection.get(ids=ids)`: ChromaDB에서 해당 ID 중 실제로 존재하는 것만 반환
- `existing`에 없는 것만 `add_documents()` 호출
- 반환값: 새로 추가된 청크 수 (전체 청크 수 아님)

### 핵심 개념: 멱등성 (Idempotency)
같은 입력으로 몇 번을 실행해도 결과가 동일한 성질.
→ 동일 문서를 10번 ingest해도 DB 상태는 1번 ingest한 것과 같음

## Q&A / 메모

<!-- 공부하면서 생긴 질문이나 메모를 여기 기록 -->
