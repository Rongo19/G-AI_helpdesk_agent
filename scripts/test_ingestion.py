
from app.rag.ingestion import ingest_documents


def main():

    chunks = ingest_documents()

    print("\n" + "=" * 60)
    print("CHUNK INSPECTION")
    print("=" * 60)

    for index, chunk in enumerate(chunks[:5]):

        print(f"\nCHUNK {index + 1}")
        print("-" * 40)

        print("Content:")
        print(chunk.page_content)

        print("\nMetadata:")
        print(chunk.metadata)

        print("\nCharacter count:")
        print(len(chunk.page_content))


if __name__ == "__main__":
    main()
