"""Ollama LLM wrapper."""
from langchain_community.llms import Ollama

from config.settings import settings


def get_llm(model: str | None = None):
    return Ollama(
        model=model or settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=settings.llm_temperature,
    )
