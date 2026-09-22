from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat


router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        response, response_type, data = process_chat(
            message=request.message,
            conversation=[
                message.model_dump()
                for message in request.conversation
            ]
        )

        return ChatResponse(
            message=response,
            type=response_type,
            data=data
        )

    except Exception as error:
        print(f"Chat error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to process your request."
        )