import requests.exceptions

from langchain_core.runnables import Runnable

from app.api.exceptions import OllamaConnectionError, VectorStoreError


class QueryService:
    def __init__(self, chain: Runnable):
        self._chain = chain

    def answer(self, question: str) -> dict:
        try:
            return self._chain.invoke(question)
        except requests.exceptions.ConnectionError as e:
            raise OllamaConnectionError("Cannot connect to Ollama. Is it running?") from e
        except Exception as e:
            raise VectorStoreError(f"Query failed: {e}") from e
