from langchain_anthropic import ChatAnthropic

from config.settings import settings


def get_llm(model: str | None = None):
    return ChatAnthropic(
        model=model or settings.llm_model,
        api_key=settings.anthropic_api_key,
        temperature=settings.llm_temperature,
    )
