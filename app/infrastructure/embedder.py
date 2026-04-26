from langchain_ollama import OllamaEmbeddings


def get_embeddings(model: str = "nomic-embed-text", base_url: str = "http://localhost:11434"):
    return OllamaEmbeddings(model=model, base_url=base_url)
