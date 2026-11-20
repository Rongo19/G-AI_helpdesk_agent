
from app.rag.retriever import (
    retrieve_documents,
    display_results
)


def main():

    print("=" * 60)
    print("GOAIFIED HR/IT - SEMANTIC RETRIEVAL TEST")
    print("=" * 60)

    query = input("\nEnter your question: ")

    print("\nSearching the policy knowledge base...")

    results = retrieve_documents(
        query=query,
        k=4
    )

    display_results(results)


if __name__ == "__main__":
    main()
