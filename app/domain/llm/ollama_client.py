from langchain_ollama import OllamaLLM

from config.settings import settings


def get_llm(model: str | None = None):
    return OllamaLLM(
        model=model or settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=settings.llm_temperature,
    )
