from langchain_core.documents import Document

from app.rag.retriever import format_retrieved_context


def test_format_retrieved_context():

    document = Document(
        page_content="Employees receive 20 annual leave days.",
        metadata={
            "source": "leave_policy.txt",
            "category": "HR"
        }
    )

    results = [(document, 0.15)]

    context = format_retrieved_context(results)

    assert "Source [1]" in context
    assert "leave_policy.txt" in context
    assert "Employees receive 20 annual leave days." in context


def test_format_empty_context():

    context = format_retrieved_context([])

    assert context == ""