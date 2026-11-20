from app.llm.client import get_llm


def main():

    print("Connecting to Groq...")

    llm = get_llm()

    response = llm.invoke(
        "Explain what Retrieval-Augmented Generation is in 3 sentences."
    )

    print("\nGroq Response:")
    print(response.content)


if __name__ == "__main__":
    main()