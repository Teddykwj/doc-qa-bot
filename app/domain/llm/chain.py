from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

CONTEXTUALIZE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Given the chat history and the latest user question, reformulate the question as a standalone question. Do not answer it, just reformulate if needed, otherwise return as is."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant for answering questions about development documentation.
Use the following context to answer the question. If you don't know the answer, say so.

Context:
{context}"""),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


class RAGChain:
    def __init__(self, retriever, llm):
        self._retriever = retriever
        self._contextualize = CONTEXTUALIZE_PROMPT | llm | StrOutputParser()
        self._answer = RAG_PROMPT | llm | StrOutputParser()

    async def _resolve_query(self, question: str, history: list[BaseMessage]) -> str:
        if not history:
            return question
        return await self._contextualize.ainvoke({"input": question, "chat_history": history})

    async def ainvoke(self, inputs: dict) -> dict:
        question: str = inputs["question"]
        history: list[BaseMessage] = inputs.get("chat_history", [])

        retrieval_query = await self._resolve_query(question, history)
        docs = await self._retriever.ainvoke(retrieval_query)
        answer = await self._answer.ainvoke({
            "context": format_docs(docs),
            "input": question,
            "chat_history": history,
        })
        sources = sorted({doc.metadata.get("source", "") for doc in docs})
        return {"answer": answer, "sources": sources}

    async def astream(self, inputs: dict):
        question: str = inputs["question"]
        history: list[BaseMessage] = inputs.get("chat_history", [])

        retrieval_query = await self._resolve_query(question, history)
        docs = await self._retriever.ainvoke(retrieval_query)
        sources = sorted({doc.metadata.get("source", "") for doc in docs})

        yield {"type": "sources", "data": sources}

        async for chunk in self._answer.astream({
            "context": format_docs(docs),
            "input": question,
            "chat_history": history,
        }):
            yield {"type": "token", "data": chunk}


def build_rag_chain(retriever, llm) -> RAGChain:
    return RAGChain(retriever, llm)
