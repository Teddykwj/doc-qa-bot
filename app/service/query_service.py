import requests.exceptions

from langchain_core.messages import BaseMessage

from app.api.exceptions import OllamaConnectionError, VectorStoreError
from app.domain.llm.chain import RAGChain


class QueryService:
    def __init__(self, chain: RAGChain):
        self._chain = chain

    async def answer(self, question: str, history: list[BaseMessage] | None = None) -> dict:
        try:
            return await self._chain.ainvoke({"question": question, "chat_history": history or []})
        except requests.exceptions.ConnectionError as e:
            raise OllamaConnectionError("Cannot connect to Ollama. Is it running?") from e
        except Exception as e:
            raise VectorStoreError(f"Query failed: {e}") from e

    async def stream(self, question: str, history: list[BaseMessage] | None = None):
        try:
            async for event in self._chain.astream({"question": question, "chat_history": history or []}):
                yield event
        except requests.exceptions.ConnectionError as e:
            raise OllamaConnectionError("Cannot connect to Ollama. Is it running?") from e
        except Exception as e:
            raise VectorStoreError(f"Stream failed: {e}") from e
