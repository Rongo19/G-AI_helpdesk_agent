import asyncio

from app.agent.graph import build_agent

from app.security.guardrails import (
    validate_user_input,
    redact_pii
)


async def main():

    print("\n===================================")
    print(" GoAified HR/IT Intelligent Agent")
    print("===================================")

    agent = build_agent()

    while True:

        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        # STEP 1: Validate employee input
        rejection = validate_user_input(question)

        if rejection:
            print("\nAssistant:", rejection)
            continue

        try:

            print("\nAgent is thinking...\n")

            # STEP 2: Invoke LangGraph agent
            result = await agent.ainvoke({
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            })

            final_message = result["messages"][-1]

            # STEP 3: Redact sensitive information
            answer = redact_pii(
                str(final_message.content)
            )

            # STEP 4: Display safe response
            print("Assistant:")
            print(answer)

        except Exception as error:

            print("\nSomething went wrong.")
            print(type(error).__name__, error)


if __name__ == "__main__":
    asyncio.run(main())