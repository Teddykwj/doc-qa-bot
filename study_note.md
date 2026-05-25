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

### RAGChain 클래스로 전환 (히스토리 + 스트리밍 지원)

LCEL 파이프만으로는 표현이 복잡해질 때 (히스토리 조건 분기, 스트리밍 등) `RAGChain` 클래스로 직접 구현.

```python
class RAGChain:
    def __init__(self, retriever, llm):
        self._retriever = retriever
        self._contextualize = CONTEXTUALIZE_PROMPT | llm | StrOutputParser()
        self._answer = RAG_PROMPT | llm | StrOutputParser()

    async def ainvoke(self, inputs: dict) -> dict: ...   # 일반 응답
    async def astream(self, inputs: dict): ...           # 스트리밍 응답 (async generator)
```

- `self._answer.astream()` — LangChain 체인의 내장 메서드. `self.astream()`과 다른 객체
- `ainvoke` / `astream` 둘 다 입력은 **한 번에** 받고, 출력만 방식이 다름

### MessagesPlaceholder

프롬프트 안에 메시지 리스트를 삽입하는 자리표시자. 대화 히스토리 전달에 사용.

```python
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "...Context:\n{context}"),
    MessagesPlaceholder("chat_history"),   # ← HumanMessage/AIMessage 리스트가 들어감
    ("human", "{input}"),
])
```

### ainvoke vs astream

| | `ainvoke` | `astream` |
|---|---|---|
| 입력 | 동일 (dict 한 번에) | 동일 |
| 출력 | 완성된 문자열 한 번에 반환 | 토큰 생성될 때마다 yield |
| 대기 | LLM이 다 끝날 때까지 | 토큰마다 즉시 |

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

## 10. 대화 히스토리 (멀티턴)

파일: `app/service/history_store.py`, `app/api/routers/query.py`

### 문제
매 질문이 독립적으로 처리됨 → "아까 말한 거 기준으로 설명해줘" 같은 후속 질문 불가

### 구조

```
클라이언트 → session_id 포함해서 요청
                ↓
            InMemoryHistoryStore.get(session_id)  → 이전 대화 목록
                ↓
            QueryService.answer(question, history)
                ↓
            RAGChain: 히스토리 있으면 질문 재구성(contextualize) → 검색 → 답변
                ↓
            store.add_exchange(session_id, question, answer)  → 히스토리 저장
```

### InMemoryHistoryStore

```python
class InMemoryHistoryStore:
    def __init__(self):
        self._store: dict[str, list[BaseMessage]] = defaultdict(list)

    def get(self, session_id: str) -> list[BaseMessage]:
        return list(self._store[session_id])  # 복사본 반환

    def add_exchange(self, session_id: str, question: str, answer: str) -> None:
        self._store[session_id].extend([
            HumanMessage(content=question),
            AIMessage(content=answer),
        ])
```

- `defaultdict(list)` — 없는 session_id 접근 시 자동으로 빈 리스트 생성
- `HumanMessage` / `AIMessage` — LangChain의 대화 메시지 타입. `MessagesPlaceholder`에 전달

### 질문 재구성 (Contextualize)

히스토리가 있을 때, 후속 질문을 단독으로 이해 가능한 질문으로 변환.

```
히스토리: "LangChain이 뭐야?" / "LangChain은 LLM 프레임워크야"
현재 질문: "그럼 LCEL은?"
     ↓ contextualize
변환 후: "LangChain에서 LCEL이란 무엇인가?"
     ↓ 이 질문으로 벡터 검색
```

```python
CONTEXTUALIZE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "reformulate the question as a standalone question..."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# 히스토리 없으면 그냥 원본 질문으로 검색
retrieval_query = (
    await contextualize_chain.ainvoke({...})
    if history else question
)
```

### session_id

- 클라이언트가 `session_id`를 보내지 않으면 서버에서 `uuid4()`로 생성해서 응답에 포함
- 클라이언트는 다음 요청 때 이 `session_id`를 다시 보내면 같은 대화 맥락 유지

---

## 11. 스트리밍 응답

파일: `app/domain/llm/chain.py`, `app/api/routers/query.py`

### 문제
LLM 응답이 완성될 때까지 (수 초) 클라이언트는 아무것도 못 받음 → 체감 응답속도 느림

### yield / 제너레이터

`yield`가 있는 함수는 **제너레이터** — `return` 처럼 값을 내보내지만 함수를 종료하지 않고 일시 정지했다가 재개.

```python
# return: 다 만든 후 한 번에 반환
def get_numbers():
    return [1, 2, 3]

# yield: 하나씩 순서대로 내보냄
def get_numbers():
    yield 1   # 일시 정지
    yield 2   # 다음 호출 때 재개
    yield 3
```

`async def` + `yield` 조합 → **비동기 제너레이터** (`async for`로 소비)

### SSE (Server-Sent Events)

서버 → 클라이언트 단방향 스트리밍 프로토콜. `text/event-stream` 형식.

```
data: {"type": "sources", "data": ["doc1.pdf"]}\n\n
data: {"type": "token", "data": "안"}\n\n
data: {"type": "token", "data": "녕"}\n\n
data: {"type": "done", "session_id": "abc-123"}\n\n
```

- 각 이벤트는 `data: <내용>\n\n` 형식 (빈 줄 2개로 구분)
- WebSocket과 달리 단방향이라 구조가 단순

### FastAPI StreamingResponse

```python
from fastapi.responses import StreamingResponse

async def event_generator():
    async for event in svc.stream(question, history):
        yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
    yield f"data: {json.dumps({'type': 'done', 'session_id': session_id})}\n\n"

return StreamingResponse(event_generator(), media_type="text/event-stream")
```

- `StreamingResponse`는 제너레이터를 받아서 생성되는 대로 HTTP 응답으로 흘려보냄
- `response_model` 사용 불가 — Pydantic 직렬화 대신 직접 `json.dumps`

### 스트리밍 흐름

```
POST /query/stream
    ↓
RAGChain.astream()
    ↓ yield {"type": "sources", "data": [...]}   ← retrieval 완료 후 즉시
    ↓ yield {"type": "token", "data": "안"}       ← LLM 토큰마다
    ↓ yield {"type": "token", "data": "녕"}
    ↓ (스트림 끝)
store.add_exchange(...)                           ← 전체 답변 완성 후 히스토리 저장
    ↓ yield {"type": "done", "session_id": "..."}
```

- retrieval(문서 검색)은 먼저 완료해야 하므로 `await`로 대기 후 sources yield
- LLM 응답만 토큰 단위로 스트리밍

### ainvoke vs astream 비교 (체인 레벨)

```python
# ainvoke: LLM이 다 끝날 때까지 기다렸다가 한 번에 반환
answer = await self._answer.ainvoke({...})
# answer = "안녕하세요"

# astream: 토큰이 생성될 때마다 즉시 yield
async for chunk in self._answer.astream({...}):
    # chunk = "안"  /  "녕"  /  "하세요"
```

입력은 동일하게 dict 한 번에 전달. 출력 방식만 다름.

---

## 12. 하이브리드 검색

파일: `app/domain/retrieval/retriever.py`

### 문제
벡터 검색만으로는 정확한 단어 매칭이 약함.

- `"ConnectionError 몇 번째 줄?"` — 고유 식별자는 의미 기반으로 못 찾음
- `"v0.2.3 변경사항"` — 버전 번호 같은 숫자/고유명사도 마찬가지

### BM25란?

키워드 기반 검색 알고리즘. 단어 빈도(TF)와 문서 희귀도(IDF)를 조합해서 점수 계산.

| | 벡터 검색 | BM25 |
|---|---|---|
| 잘하는 것 | 의미 유사도, 동의어, 문맥 | 정확한 단어 매칭, 고유명사, 코드 식별자 |
| 못하는 것 | 정확한 단어 매칭 | 의미 기반 유사도 |

### RRF (Reciprocal Rank Fusion)

두 검색 결과의 순위를 점수로 변환해서 합산하는 방식. 스케일이 다른 두 점수를 직접 더하는 것보다 안정적.

```python
rrf_score = 1/(rank_in_bm25 + 60) + 1/(rank_in_vector + 60)
```

- `60`은 상수 (rrf_k) — 높을수록 1위와 하위 순위 간 점수 차이가 줄어듦
- 두 검색 모두에서 상위에 오른 문서가 최종 상위권 차지

```
벡터 검색 결과: [문서A(1위), 문서C(2위), 문서E(3위)]
BM25 결과:     [문서B(1위), 문서A(2위), 문서D(3위)]

RRF 합산:
  문서A = 1/(1+60) + 1/(2+60) = 0.0164 + 0.0161 = 0.0325  ← 1위
  문서B = 1/(1+60)             = 0.0164             ← 2위
  문서C = 1/(2+60)             = 0.0161             ← 3위
```

### HybridRetriever 구현

`EnsembleRetriever`가 현재 LangChain 버전에 없어서 직접 구현.

```python
class HybridRetriever(BaseRetriever):
    bm25: BM25Retriever
    vector: BaseRetriever
    k: int = 4
    rrf_k: int = 60

    def _get_relevant_documents(self, query, ...) -> list[Document]:
        bm25_docs = self.bm25.invoke(query)
        vector_docs = self.vector.invoke(query)

        scores: dict[str, float] = {}
        doc_map: dict[str, Document] = {}

        for rank, doc in enumerate(bm25_docs):
            key = doc.page_content
            scores[key] = scores.get(key, 0) + 1 / (rank + self.rrf_k)
            doc_map[key] = doc

        for rank, doc in enumerate(vector_docs):
            key = doc.page_content
            scores[key] = scores.get(key, 0) + 1 / (rank + self.rrf_k)
            doc_map[key] = doc

        ranked = sorted(scores, key=lambda k: scores[k], reverse=True)
        return [doc_map[key] for key in ranked[:self.k]]
```

- `page_content`를 key로 중복 제거 + RRF 합산
- `BaseRetriever`를 상속하면 LangChain 체인에 그대로 연결 가능

### BM25 인덱스 구성

BM25는 인메모리 — 서버 시작 시 ChromaDB에서 전체 청크를 읽어 인덱스 구성.

```python
def get_hybrid_retriever(vectorstore, k=4):
    result = vectorstore._collection.get(include=["documents", "metadatas"])
    docs = [Document(page_content=text, metadata=meta or {}) for text, meta in ...]

    if not docs:
        return get_retriever(vectorstore, k=k)  # fallback

    bm25 = BM25Retriever.from_documents(docs, k=k)
    vector = get_retriever(vectorstore, k=k)
    return HybridRetriever(bm25=bm25, vector=vector, k=k)
```

### 주의: BM25 인덱스 갱신 시점

`lru_cache`로 서버 시작 시 한 번만 생성. 새 문서를 ingest해도 BM25에는 즉시 반영되지 않음.
→ 벡터 검색은 즉시 반영, BM25는 서버 재시작 후 반영.

---

## 13. 자동 인제스트 스케줄러

파일: `app/service/scheduler.py`, `app/main.py`, `config/settings.py`

### 목적
스크래핑 → 인제스트를 주기적으로 자동 실행해서 문서를 최신 상태로 유지.

### APScheduler

Python 프로세스 내부에서 동작하는 스케줄러 라이브러리. 별도 인프라(Redis 등) 없이 FastAPI 서버 안에서 함께 실행.

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.add_job(_run_ingest, "cron", hour=3)  # 매일 새벽 3시
scheduler.start()
```

- `AsyncIOScheduler` — FastAPI의 이벤트 루프와 같은 루프에서 실행
- `"cron"` — 리눅스 cron처럼 주기 지정. `hour`, `minute`, `day_of_week` 등 조합 가능

### 인제스트 후 BM25 캐시 무효화

새 문서가 추가되면 `lru_cache`로 고정된 `_query_service`를 재생성해야 BM25 인덱스에 반영됨.

```python
async def _run_ingest() -> None:
    try:
        count = await _ingest_service().run()
        if count > 0:
            _query_service.cache_clear()  # 다음 요청 시 HybridRetriever 재구성
        logger.info("Scheduled ingest complete: %d new chunks", count)
    except Exception as e:
        logger.error("Scheduled ingest failed: %s", e)
```

- `cache_clear()` — `lru_cache`가 붙은 함수에 자동으로 생기는 메서드. 캐시를 비워서 다음 호출 시 재생성하게 함
- 예외가 나도 서버는 계속 실행 — 스케줄 작업 실패가 서버를 죽이면 안 되므로 `try/except`로 처리

### @asynccontextmanager + lifespan

FastAPI의 lifespan: 서버 시작/종료 시점에 실행할 코드를 등록하는 방식.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── 서버 시작 시 ──
    scheduler = create_scheduler(hour=settings.ingest_schedule_hour)
    scheduler.start()

    yield  # 서버가 실행되는 동안 여기서 대기

    # ── 서버 종료 시 ──
    scheduler.shutdown()

app = FastAPI(title="Doc QA Bot", lifespan=lifespan)
```

**@asynccontextmanager**
- `yield` 앞 = `__aenter__` (시작 로직)
- `yield` 뒤 = `__aexit__` (종료 로직)
- 예외가 발생해도 `yield` 뒤 코드는 반드시 실행 (`try/finally`와 동일한 보장)
- 클래스로 `__aenter__` / `__aexit__`를 직접 구현하는 대신 제너레이터 함수 하나로 대체

### 설정

`config/settings.py`에서 시각 관리. `.env`로 오버라이드 가능.

```python
ingest_schedule_hour: int = 3  # 기본값: 새벽 3시
```

```
# .env
INGEST_SCHEDULE_HOUR=6
```

### 한계

- 서버가 죽으면 스케줄도 같이 멈춤 (Celery Beat는 독립 프로세스라 이 문제 없음)
- 실행 이력 저장 없음 — 실패해도 로그만 남고 재시도 없음
- BM25 캐시 무효화 후 첫 요청 시 재구성 비용 발생 (전체 청크 재로딩)

---

## Q&A / 메모

<!-- 공부하면서 생긴 질문이나 메모를 여기 기록 -->
