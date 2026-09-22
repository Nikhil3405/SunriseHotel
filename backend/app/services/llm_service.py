import json
import os

from dotenv import load_dotenv
from groq import Groq

from app.services.tools import (
    hotel_info,
    room_info,
    suitable_rooms,
    availability,
)

load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = os.getenv("GROQ_MODEL")


SYSTEM_PROMPT = """
You are the guest assistant for Sunrise Hotel.

Your job is to help guests with questions about:
- hotel information
- amenities
- rooms
- policies
- breakfast
- room availability

You have access to tools that provide authoritative hotel information.

IMPORTANT RULES:

1. Use the appropriate tool whenever the answer depends on
   hotel data.

2. Treat tool results as the authoritative source of truth.

3. Never contradict, modify, or invent information contained
   in a tool result.

4. For room-specific questions, use room_info with the room name.

5. For questions asking which rooms can accommodate a number
   of guests, use suitable_rooms.

6. For availability questions, ALWAYS use the availability tool.

7. Never determine availability from general room information.

8. If the availability tool returns available=true, the rooms
   in its rooms list are available.

9. If the availability tool returns available=false, do not
   claim that any room is available.

10. When reporting room features such as breakfast, beds,
    capacity or price, use only information returned by the
    room information or availability tools.

11. Do not assume that missing information means something is
    unavailable. If the hotel data does not contain information
    about something, say that you do not have information about it.

12. Never invent hotel amenities, room features, prices,
    policies, services or availability.

13. Use conversation history to understand follow-up questions.

14. Be concise, friendly and helpful.
AVAILABILITY DATE RULES:
15. If a guest provides a date without a year, assume 2026.
16. If a guest explicitly provides a year, use the year they provided.
17. Never invent a different year when the guest has not provided one.
18. Availability must always be checked using the availability tool.
19. If the requested dates are outside the available mock calendar, clearly tell the guest that availability data is not available for those dates.
20. If the requested dates are within the available mock calendar, but the availability tool returns available=false, do not claim that any room is available.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "hotel_info",
            "description": (
                "Get information about Sunrise Hotel, including "
                "amenities, breakfast, policies, services, restaurants, "
                "check-in, check-out, accessibility and contact information."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "room_info",
            "description": (
                "Get detailed information about one specific hotel room, "
                "including its capacity, beds, price, breakfast inclusion "
                "and room amenities."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "room_name": {
                        "type": "string",
                        "description": (
                            "Exact or natural-language name of the room, "
                            "such as Deluxe Room, Family Suite or Premium Suite."
                        )
                    }
                },
                "required": [
                    "room_name"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "suitable_rooms",
            "description": (
                "Find all hotel rooms that can accommodate the specified "
                "number of guests. Use this when the guest asks which rooms "
                "are suitable for a certain number of guests."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "guests": {
                        "type": "integer",
                        "description": "Number of guests."
                    }
                },
                "required": [
                    "guests"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "availability",
            "description": (
                "Check actual room availability for specific check-in and "
                "check-out dates and number of guests. The result is "
                "authoritative. If available is true, the rooms in the "
                "rooms list are available. If available is false, there "
                "are no available rooms for the requested stay."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "check_in": {
                        "type": "string",
                        "description": "Check-in date in YYYY-MM-DD format."
                    },
                    "check_out": {
                        "type": "string",
                        "description": "Check-out date in YYYY-MM-DD format."
                    },
                    "guests": {
                        "type": "integer",
                        "description": "Number of guests."
                    }
                },
                "required": [
                    "check_in",
                    "check_out",
                    "guests"
                ]
            }
        }
    }
]

TOOL_FUNCTIONS = {
    "hotel_info": hotel_info,
    "room_info": room_info,
    "suitable_rooms": suitable_rooms,
    "availability": availability,
}

def execute_tool(tool_name: str, arguments: dict) -> dict:
    tool = TOOL_FUNCTIONS.get(tool_name)

    if tool is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    return tool(**arguments)


def format_availability_response(result):
    if not result["available"]:
        message = (
            f"Sorry, there are no available rooms for "
            f"{result['guests']} guests from "
            f"{result['check_in']} to {result['check_out']}."
        )
    else:
        room_count = len(result["rooms"])

        lines = [
            f"I found {room_count} available room(s) for "
            f"{result['guests']} guests from "
            f"{result['check_in']} to {result['check_out']}."
        ]

        for room in result["rooms"]:
            breakfast = (
                "Breakfast included"
                if room["breakfast_included"]
                else "Breakfast not included"
            )

            lines.append(
                f"- {room['name']} — "
                f"{room['price_per_night']} {room['currency']}/night — "
                f"{breakfast}"
            )

        message = "\n".join(lines)

    return message, "availability", result

def generate_response(
    message: str,
    conversation: list[dict] | None = None
) -> tuple[str, str, dict | None]:

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    if conversation:
        messages.extend(conversation)

    messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0
    )

    assistant_message = response.choices[0].message

    if not assistant_message.tool_calls:
        return assistant_message.content or "", "answer", None

    messages.append(assistant_message)

    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        tool_result = execute_tool(
            tool_name=tool_name,
            arguments=arguments
        )

        # Availability is deterministic.
        # Do not ask the LLM to reinterpret the result.
        if tool_name == "availability":
            return format_availability_response(tool_result)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": json.dumps(tool_result)
            }
        )

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    return (
        final_response.choices[0].message.content or "",
        "answer",None
    )