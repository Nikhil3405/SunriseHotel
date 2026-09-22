from app.services.llm_service import generate_response


def test_hotel_question():
    response, response_type, data = generate_response(
        "What time is check-in?"
    )

    assert response
    assert response_type == "answer"
    assert data is None
    assert "2:00" in response


def test_room_question():
    response, response_type, data = generate_response(
        "Which room can accommodate 4 guests?"
    )

    assert response
    assert response_type == "answer"
    assert data is None
    assert (
        "Family Suite" in response
        or "Premium Suite" in response
    )


def test_availability_question():
    response, response_type, data = generate_response(
        "Do you have a room available from October 10 to October 12 for 3 guests?"
    )

    assert response
    assert response_type == "availability"
    assert data is not None

    assert data["available"] is True
    assert data["check_in"] == "2026-10-10"
    assert data["check_out"] == "2026-10-12"
    assert data["guests"] == 3
    assert len(data["rooms"]) == 3