from app.services.room_service import (
    get_room_info,
    get_suitable_rooms,
)


def test_get_specific_room():
    room = get_room_info("Deluxe Room")

    assert room is not None
    assert room["name"] == "Deluxe Room"
    assert room["breakfast_included"] is True


def test_room_name_is_case_insensitive():
    room = get_room_info("deluxe room")

    assert room is not None
    assert room["name"] == "Deluxe Room"


def test_unknown_room():
    room = get_room_info("Presidential Room")

    assert room is None


def test_suitable_rooms():
    rooms = get_suitable_rooms(4)

    names = [room["name"] for room in rooms]

    assert "Family Suite" in names
    assert "Premium Suite" in names
    assert "Standard Room" not in names
    assert "Deluxe Room" not in names