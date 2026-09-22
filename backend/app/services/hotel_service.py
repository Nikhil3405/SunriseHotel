import json
from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "hotel.json"


def get_hotel_info() -> dict:
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)["hotel"]