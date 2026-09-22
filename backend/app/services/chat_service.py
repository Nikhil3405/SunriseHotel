from app.services.llm_service import generate_response


def process_chat(
    message: str,
    conversation: list[dict]
) -> tuple[str, str, dict | None]:
    return generate_response(
        message=message,
        conversation=conversation
    )