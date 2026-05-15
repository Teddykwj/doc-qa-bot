import requests.exceptions

from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable

from app.api.exceptions import OllamaConnectionError, VectorStoreError


class QueryService:
    def __init__(self, chain: Runnable):
        self._chain = chain

    async def answer(self, question: str, history: list[BaseMessage] | None = None) -> dict:
        try:
            return await self._chain.ainvoke({"question": question, "chat_history": history or []})
        except requests.exceptions.ConnectionError as e:
            raise OllamaConnectionError("Cannot connect to Ollama. Is it running?") from e
        except Exception as e:
            raise VectorStoreError(f"Query failed: {e}") from e
