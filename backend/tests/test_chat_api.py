from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_request_validation():
    response = client.post(
        "/api/chat",
        json={"message": ""}
    )

    assert response.status_code == 422


def test_chat_availability_response():
    response = client.post(
        "/api/chat",
        json={
            "message": (
                "Do you have a room from October 10 to October 12 "
                "for 3 guests?"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["type"] == "availability"
    assert data["data"] is not None
    assert data["data"]["check_in"] == "2026-10-10"
    assert data["data"]["check_out"] == "2026-10-12"
    assert data["data"]["guests"] == 3
    assert len(data["data"]["rooms"]) == 3


def test_chat_accepts_conversation_context():
    response = client.post(
        "/api/chat",
        json={
            "message": "Does it include breakfast?",
            "conversation": [
                {
                    "role": "user",
                    "content": "Tell me about the Deluxe Room."
                },
                {
                    "role": "assistant",
                    "content": (
                        "The Deluxe Room accommodates up to 3 guests."
                    )
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"]
    assert data["type"] == "answer"