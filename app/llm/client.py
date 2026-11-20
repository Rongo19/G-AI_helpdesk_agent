from langchain_groq import ChatGroq

from app.config import settings


def get_llm() -> ChatGroq:

    llm = ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key.get_secret_value(),
        temperature=0,
        max_retries=2,
        timeout=30
    )

    return llm