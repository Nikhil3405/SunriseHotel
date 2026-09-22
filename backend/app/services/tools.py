from datetime import date

from app.services.hotel_service import get_hotel_info
from app.services.room_service import (
    get_room_info,
    get_suitable_rooms,
)
from app.services.availability_service import check_availability


def hotel_info() -> dict:
    return get_hotel_info()


def room_info(room_name: str) -> dict | None:
    return get_room_info(room_name)


def suitable_rooms(guests: int) -> list[dict]:
    return get_suitable_rooms(guests)


def availability(
    check_in: str,
    check_out: str,
    guests: int
) -> dict:
    check_in_date = date.fromisoformat(check_in)
    check_out_date = date.fromisoformat(check_out)

    return check_availability(
        check_in=check_in_date,
        check_out=check_out_date,
        guests=guests
    )