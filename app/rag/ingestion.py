from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Project directories
BASE_DIR = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = BASE_DIR / "documents"


def get_document_category(filename: str) -> str:
    """Identify whether a document belongs to HR or IT."""

    filename = filename.lower()

    if any(word in filename for word in [
        "leave", "employee", "work_from_home", "hr"
    ]):
        return "HR"

    if any(word in filename for word in [
        "it", "security", "technical"
    ]):
        return "IT"

    return "GENERAL"


def load_documents() -> list[Document]:
    """Load TXT and PDF policy documents."""

    documents = []

    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"Documents directory not found: {DOCUMENTS_DIR}"
        )

    for file_path in sorted(DOCUMENTS_DIR.iterdir()):

        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()

        if extension == ".txt":
            loader = TextLoader(
                str(file_path),
                encoding="utf-8"
            )

        elif extension == ".pdf":
            loader = PyPDFLoader(str(file_path))

        else:
            print(f"Skipping unsupported file: {file_path.name}")
            continue

        loaded_docs = loader.load()

        for document in loaded_docs:

            document.metadata.update({
                "source": file_path.name,
                "category": get_document_category(file_path.name),
                "file_type": extension.lstrip(".")
            })

        documents.extend(loaded_docs)

        print(
            f"Loaded {file_path.name}: "
            f"{len(loaded_docs)} document page(s)"
        )

    if not documents:
        raise ValueError(
            "No supported policy documents were found."
        )

    return documents


def split_documents(
    documents: list[Document]
) -> list[Document]:
    """Split documents into smaller chunks."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=75,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = index

    return chunks


def ingest_documents() -> list[Document]:
    """Load policy documents and split them into chunks."""

    documents = load_documents()

    print(f"\nTotal documents loaded: {len(documents)}")

    chunks = split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    return chunks
