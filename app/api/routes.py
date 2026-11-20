from fastapi import APIRouter, HTTPException, Request

from app.api.schemas import ChatRequest, ChatResponse

from app.security.guardrails import (
    validate_user_input,
    redact_pii
)


router = APIRouter(prefix="/api", tags=["Helpdesk"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    request: Request
):

    # Step 1: Validate input
    rejection = validate_user_input(payload.question)

    if rejection:
        return ChatResponse(
            answer=rejection,
            status="blocked"
        )

    try:

        # Step 2: Get the initialized agent
        agent = request.app.state.agent

        # Step 3: Execute the agent
        result = await agent.ainvoke({
            "messages": [
                {
                    "role": "user",
                    "content": payload.question
                }
            ]
        })

        # Step 4: Extract the final response
        final_message = result["messages"][-1]

        answer = str(final_message.content)

        # Step 5: Redact PII
        answer = redact_pii(answer)

        # Step 6: Return response
        return ChatResponse(
            answer=answer,
            status="success"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question."
        )