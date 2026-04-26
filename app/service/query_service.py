from langchain_core.runnables import Runnable


class QueryService:
    def __init__(self, chain: Runnable):
        self._chain = chain

    def answer(self, question: str) -> str:
        return self._chain.invoke(question)
