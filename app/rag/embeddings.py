
from langchain_huggingface import HuggingFaceEmbeddings


# Embedding model configuration
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Initialize and return the Hugging Face embedding model.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,

        model_kwargs={
            "device": "cpu"
        },

        encode_kwargs={
            "normalize_embeddings": True,
            "batch_size": 32
        }
    )

    return embeddings
