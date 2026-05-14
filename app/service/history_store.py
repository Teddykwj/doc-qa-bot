from collections import defaultdict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


class InMemoryHistoryStore:
    def __init__(self):
        self._store: dict[str, list[BaseMessage]] = defaultdict(list)

    def get(self, session_id: str) -> list[BaseMessage]:
        return list(self._store[session_id])

    def add_exchange(self, session_id: str, question: str, answer: str) -> None:
        self._store[session_id].extend([
            HumanMessage(content=question),
            AIMessage(content=answer),
        ])
