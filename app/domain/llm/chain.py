from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda

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


def build_rag_chain(retriever, llm):
    contextualize_chain = CONTEXTUALIZE_PROMPT | llm | StrOutputParser()
    answer_chain = RAG_PROMPT | llm | StrOutputParser()

    async def _run(inputs: dict) -> dict:
        question: str = inputs["question"]
        history: list[BaseMessage] = inputs.get("chat_history", [])

        retrieval_query = (
            await contextualize_chain.ainvoke({"input": question, "chat_history": history})
            if history else question
        )

        docs = await retriever.ainvoke(retrieval_query)
        answer = await answer_chain.ainvoke({
            "context": format_docs(docs),
            "input": question,
            "chat_history": history,
        })
        sources = sorted({doc.metadata.get("source", "") for doc in docs})
        return {"answer": answer, "sources": sources}

    return RunnableLambda(_run)
