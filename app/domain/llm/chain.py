from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

RAG_PROMPT = ChatPromptTemplate.from_template(
    """You are a helpful assistant for answering questions about development documentation.
Use the following context to answer the question. If you don't know the answer, say so.

Context:
{context}

Question: {question}

Answer:"""
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(retriever, llm):
    answer_chain = RAG_PROMPT | llm | StrOutputParser()

    def _run(question: str) -> dict:
        docs = retriever.invoke(question)
        answer = answer_chain.invoke({"context": format_docs(docs), "question": question})
        sources = sorted({doc.metadata.get("source", "") for doc in docs})
        return {"answer": answer, "sources": sources}

    return RunnableLambda(_run)
