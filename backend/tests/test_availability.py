from datetime import date

from app.services.availability_service import check_availability


def test_three_guests_can_find_available_room():
    result = check_availability(
        check_in=date(2026, 10, 10),
        check_out=date(2026, 10, 12),
        guests=3
    )

    assert result["available"] is True

    room_names = [
        room["name"]
        for room in result["rooms"]
    ]

    assert "Deluxe Room" in room_names
    assert "Family Suite" in room_names


def test_room_capacity_is_respected():
    result = check_availability(
        check_in=date(2026, 10, 10),
        check_out=date(2026, 10, 12),
        guests=5
    )

    assert result["available"] is True

    room_names = [
        room["name"]
        for room in result["rooms"]
    ]

    assert "Family Suite" in room_names
    assert "Standard Room" not in room_names
    assert "Deluxe Room" not in room_names


def test_unavailable_dates():
    result = check_availability(
        check_in=date(2026, 10, 15),
        check_out=date(2026, 10, 17),
        guests=3
    )

    assert result["available"] is False
    assert result["rooms"] == []


def test_invalid_dates():
    try:
        check_availability(
            check_in=date(2026, 10, 12),
            check_out=date(2026, 10, 10),
            guests=2
        )
        assert False
    except ValueError as error:
        assert str(error) == "Check-out date must be after check-in date."


def test_invalid_guest_count():
    try:
        check_availability(
            check_in=date(2026, 10, 10),
            check_out=date(2026, 10, 12),
            guests=0
        )
        assert False
    except ValueError as error:
        assert str(error) == "Number of guests must be at least 1."