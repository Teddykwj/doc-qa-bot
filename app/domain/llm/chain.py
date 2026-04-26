from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

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
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )
