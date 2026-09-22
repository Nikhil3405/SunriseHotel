import json
from datetime import date, timedelta
from pathlib import Path

from app.services.room_service import get_rooms



DATA_PATH = Path(__file__).parent.parent / "data" / "availability.json"


def load_availability() -> dict:
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)["availability"]


def get_dates(check_in: date, check_out: date) -> list[str]:
    dates = []
    current = check_in

    while current < check_out:
        dates.append(current.isoformat())
        current += timedelta(days=1)

    return dates


def check_availability(
    check_in: date,
    check_out: date,
    guests: int
) -> dict:

    # Basic validation
    if check_in >= check_out:
        raise ValueError("Check-out date must be after check-in date.")

    if guests < 1:
        raise ValueError("Number of guests must be at least 1.")

    rooms = get_rooms()
    availability = load_availability()

    requested_dates = get_dates(check_in, check_out)

    available_rooms = []

    for room in rooms:
        # Guest capacity check
        if room["max_guests"] < guests:
            continue

        room_inventory = availability.get(room["id"], {})

        # Room must have inventory on every requested night
        is_available = all(
            room_inventory.get(date, 0) > 0
            for date in requested_dates
        )

        if is_available:
            available_rooms.append({
                "room_id": room["id"],
                "name": room["name"],
                "description": room["description"],
                "max_guests": room["max_guests"],
                "price_per_night": room["price_per_night"],
                "currency": room["currency"],
                "breakfast_included": room["breakfast_included"],
                "beds": room["beds"]
            })

    return {
        "available": len(available_rooms) > 0,
        "check_in": check_in.isoformat(),
        "check_out": check_out.isoformat(),
        "guests": guests,
        "rooms": available_rooms
    }