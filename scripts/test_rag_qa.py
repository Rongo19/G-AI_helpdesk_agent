from app.rag.qa import answer_policy_question


def main():

    print("\n=== GoAified HR/IT Helpdesk ===")

    question = input("\nAsk your question: ")

    result = answer_policy_question(question)

    print("\n--- ANSWER ---")
    print(result["answer"])

    print("\n--- SOURCES ---")

    for source in result["sources"]:
        print(
            f'{source["reference"]} '
            f'{source["filename"]} '
            f'({source["category"]})'
        )


if __name__ == "__main__":
    main()