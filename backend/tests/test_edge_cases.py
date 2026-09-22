from datetime import date

import pytest

from app.services.availability_service import check_availability
from app.services.room_service import get_room_info


def test_invalid_date_range():
    with pytest.raises(
        ValueError,
        match="Check-out date must be after check-in date",
    ):
        check_availability(
            check_in=date(2026, 10, 12),
            check_out=date(2026, 10, 10),
            guests=2,
        )


def test_invalid_guest_count():
    with pytest.raises(
        ValueError,
        match="Number of guests must be at least 1",
    ):
        check_availability(
            check_in=date(2026, 10, 10),
            check_out=date(2026, 10, 12),
            guests=0,
        )


def test_unknown_room():
    result = get_room_info("Helicopter Suite")

    assert result is None