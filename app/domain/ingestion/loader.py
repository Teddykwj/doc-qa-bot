from pathlib import Path
from typing import List

from langchain_community.document_loaders import DirectoryLoader, TextLoader, UnstructuredMarkdownLoader, PyPDFLoader
from langchain_core.documents import Document


def load_documents(source_dir: str) -> List[Document]:
    source_path = Path(source_dir)
    loaders = {
        "**/*.md": UnstructuredMarkdownLoader,
        "**/*.txt": TextLoader,
        "**/*.pdf": PyPDFLoader,
    }
    docs = []
    for glob_pattern, loader_cls in loaders.items():
        loader = DirectoryLoader(str(source_path), glob=glob_pattern, loader_cls=loader_cls, silent_errors=True)
        docs.extend(loader.load())
    return docs
