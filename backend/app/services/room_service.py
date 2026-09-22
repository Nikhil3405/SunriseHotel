import json
from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "rooms.json"


def get_rooms() -> list[dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)["rooms"]


def get_room_info(room_name: str) -> dict | None:
    rooms = get_rooms()

    normalized_name = room_name.strip().lower()

    for room in rooms:
        if room["name"].lower() == normalized_name:
            return room

    return None


def get_suitable_rooms(guests: int) -> list[dict]:
    rooms = get_rooms()

    return [
        room
        for room in rooms
        if room["max_guests"] >= guests
    ]