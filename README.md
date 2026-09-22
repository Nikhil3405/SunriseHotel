# Sunrise Hotel Guest Assistant

An AI-powered hotel guest assistant that helps guests get hotel information and check room availability through a conversational web interface.

## Live Demo

- **Frontend:** https://sunrise-hotel-co65.vercel.app/
- **Backend:** https://sunrise-hotel-ten.vercel.app/

The frontend is deployed on Vercel and communicates with the FastAPI backend through `/health` and `/api/chat`.

---

## Overview

The assistant helps guests with:

- Hotel amenities and services
- Room information and suitability
- Breakfast
- Check-in and check-out
- Hotel policies
- Room availability
- Follow-up questions

Core design principle:

> **Use AI for natural-language understanding and tool selection, while keeping business-critical decisions deterministic.**

## Guest Journey

```text
Guest
  ↓
Next.js Chat UI
  ↓
FastAPI /api/chat
  ↓
Groq LLM
  ↓
Tool selection
  ↓
Python tool execution
  ↓
JSON hotel data
  ↓
Response
  ↓
Frontend
```

For availability:

```text
Guest request → LLM identifies intent → availability tool
→ validate dates/guests → check every night → return rooms → room cards
```

The LLM does **not** decide whether a room is actually available.

---

## Features

### Conversational Assistant

Guests can ask natural-language questions such as:

```text
What time is check-in?
Does the hotel have a swimming pool?
What restaurants are available?
What is the cancellation policy?
Is breakfast included in the Deluxe Room?
```

### Room Information

The assistant provides room type, maximum guests, beds, size, price, breakfast inclusion, and room features.

### Room Suitability

Example:

```text
Which room can accommodate 3 guests?
```

The backend determines suitable rooms from configured capacity.

### Availability

Guests provide check-in date, check-out date, and guest count. The backend checks inventory for the complete stay and the frontend displays structured room cards.

### Conversation Context

Previous messages are sent to the backend so follow-ups can be understood.

### UX and Error States

The frontend includes loading states, backend connection states, API error handling, unsupported-information fallback, suggested questions, responsive layout, and an independent chat scroll area.

---

## Technology Stack

### Frontend

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS 4
- Lucide React
- React Markdown
- Remark GFM

### Backend

- Python
- FastAPI
- Pydantic
- Pytest

### AI

- Groq API
- `openai/gpt-oss-120b`

### Data

The hotel knowledge base is stored as JSON:

```text
backend/app/data/
├── hotel.json
├── rooms.json
└── availability.json
```

JSON was chosen because the knowledge base is small and structured. A production system could replace it with a database or hotel/property management system.

---

## Architecture

```text
┌─────────────────────┐
│        Guest        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   Next.js Frontend  │
│ Chat / Loading / UI │
└──────────┬──────────┘
           │ HTTP / JSON
           ↓
┌─────────────────────┐
│    FastAPI Backend  │
│ API / Validation    │
│ Conversation Context│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│      Groq LLM       │
│ Intent / Tool Select│
│ Response Generation │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│    Python Tools     │
│ hotel_info()        │
│ room_info()         │
│ suitable_rooms()    │
│ availability()      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│      JSON Data      │
└─────────────────────┘
```

---

## AI and Tool Calling

The LLM is responsible for natural-language understanding, intent identification, tool selection, conversation context, and natural-language response generation.

It is **not** responsible for directly accessing files, deciding room inventory, determining availability, or inventing hotel information.

Available tools:

```text
hotel_info()
room_info(room_name)
suitable_rooms(guests)
availability(check_in, check_out, guests)
```

The Python backend executes the selected tool and uses its result as authoritative data.

### Why AI?

Guests can express the same request in different ways:

```text
Do you have anything for three people?
Which room works for 3 guests?
We are a group of three. What can we book?
```

The LLM handles this natural-language understanding and maps the request to the appropriate backend operation.

---

## Deterministic Availability

Availability is intentionally handled outside the LLM.

For example:

```text
Check-in: 2026-10-10
Check-out: 2026-10-12
Guests: 3
```

The backend:

1. Validates dates and guest count.
2. Generates every night in the requested stay.
3. Filters rooms by maximum guest capacity.
4. Checks inventory for every requested night.
5. Returns only rooms available for the complete stay.

If a room is available on October 10 but unavailable on October 11, it is not returned for an October 10–12 stay.

This makes availability deterministic and testable.

---

## Hallucination Prevention

Hotel information is treated as authoritative data. The assistant is instructed to:

- Use tools whenever hotel data is required.
- Never invent amenities, room features, prices, policies, services, or availability.
- Never contradict tool results.
- Use room-specific tools for room-specific questions.
- Use the availability tool for availability requests.
- Avoid treating missing information as false.

The system distinguishes between **known false** and **information not available**.

For example, airport shuttle availability is explicitly stored as false, so the assistant can say it is unavailable. If helicopter transportation is not present in the data, the assistant should say it does not have information about the service instead of assuming it is unavailable.

---

## Error Handling

The application handles:

- Backend connection failures
- API failures
- AI/model failures
- Invalid availability requests
- Unsupported hotel information

The frontend shows user-friendly errors instead of internal server details. The chat remains disabled until the startup health check succeeds.

### Health Check

```http
GET /health
```

Response:

```json
{"status":"ok"}
```

---

## Backend API

### Chat

```http
POST /api/chat
```

Request:

```json
{
  "message": "What time is check-in?",
  "conversation": []
}
```

Example:

```bash
curl -X POST https://sunrise-hotel-ten.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What time is check-in?","conversation":[]}'
```

Response:

```json
{
  "message": "Check-in at Sunrise Hotel is at 2:00 PM.",
  "type": "answer",
  "data": null
}
```

Availability responses use structured data so the frontend can render room cards without relying on the LLM to reinterpret inventory.

---

## Project Structure

```text
hotel/
├── backend/
│   ├── app/
│   │   ├── api/chat.py
│   │   ├── data/
│   │   │   ├── hotel.json
│   │   │   ├── rooms.json
│   │   │   └── availability.json
│   │   ├── schemas/chat.py
│   │   ├── services/
│   │   │   ├── availability_service.py
│   │   │   ├── chat_service.py
│   │   │   ├── hotel_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── room_service.py
│   │   │   └── tools.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_availability.py
│   │   ├── test_chat_api.py
│   │   ├── test_edge_cases.py
│   │   ├── test_llm.py
│   │   └── test_room_service.py
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── types/
│   ├── public/
│   ├── .env.example
│   └── package.json
└── README.md
```

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js and npm
- Groq API key

### Backend

```bash
cd backend
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Install and run:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Create `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Backend: `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Frontend: `http://localhost:3000`

The Groq API key is kept exclusively on the backend. Only `.env.example` files are committed.

---

## Testing

Run:

```bash
python -m pytest -q
```

Current result:

```text
19 passed, 2 warnings
```

The warnings are dependency deprecation warnings and are not test failures.

The frontend production build was also verified:

```bash
npm run build
```

Result:

```text
✓ Compiled successfully
✓ Finished TypeScript
✓ Generating static pages
✓ Finalizing page optimization
```

---

## Evaluation Scenarios

| # | Scenario | Expected Behavior |
|---|---|---|
| 1 | Ask for check-in time | Returns hotel check-in time |
| 2 | Ask about amenities | Retrieves hotel knowledge |
| 3 | Ask about room breakfast | Uses room-specific information |
| 4 | Ask which room supports 3 guests | Returns suitable rooms |
| 5 | Check availability | Uses deterministic availability tool |
| 6 | Ask a follow-up | Uses conversation context |
| 7 | Outside mock calendar | States availability data is unavailable |
| 8 | Unknown hotel information | Does not invent an answer |
| 9 | Missing/invalid availability information | Requests or validates required information |
| 10 | Backend/API failure | Shows useful frontend error state |

---

## Product and Engineering Decisions

### Why conversational UI?

Guests naturally ask questions in normal language. Chat reduces the need to navigate through multiple hotel pages.

### Why structured availability cards?

Guests can quickly scan room name, capacity, beds, price, and breakfast inclusion instead of interpreting a long paragraph.

### Why JSON instead of a database?

The assignment has a small structured knowledge base. JSON is simple to inspect, modify, test, and deploy.

### Why not RAG?

The knowledge base is small and structured. Embeddings and a vector database would add complexity without significant value for this scope.

### Why keep availability outside the LLM?

Availability is business-critical and deterministic. Python performs the inventory calculation, making behavior predictable and testable.

---

## Measuring Usefulness

For a real deployment, useful metrics could include:

- Successful question-answer rate
- Availability lookup completion rate
- Fallback rate
- AI/model failure rate
- Response latency
- Human-assistance rate
- Guest satisfaction
- Repeated-question frequency

---

## Production Improvements

Before real hotel deployment, I would consider:

- Real hotel/property management integration
- Booking and cancellation workflow
- Structured logging, metrics, and tracing
- API rate limiting
- Automated AI evaluation for factual accuracy and tool selection
- Multilingual support
- Human-agent handoff

These were intentionally kept outside the assignment scope to keep the implementation focused and maintainable.

---

## Deployment

### Frontend

https://sunrise-hotel-co65.vercel.app/

### Backend

https://sunrise-hotel-ten.vercel.app/

The frontend uses `NEXT_PUBLIC_API_URL` to communicate with the backend. On startup it calls `GET /health` before enabling chat, which also helps when the backend has temporarily gone idle.

---

## Security

The Groq API key is never exposed to the frontend.

```text
Browser → Next.js → FastAPI → Groq API
```

The API key exists only in the backend environment.

---

## AI Tools Used During Development

AI-assisted development tools were used for architecture planning, code generation, debugging, test scenario design, UI refinement, error analysis, and documentation assistance. Technical and product decisions were validated through implementation, testing, and production builds.

---

## Final Validation

- **Backend:** 19 tests passed
- **Frontend:** Production build successful
- Hotel information tested
- Room information tested
- Room suitability tested
- Availability tested
- Follow-up questions tested
- Unsupported information tested
- Loading and backend connection states tested
- API error handling tested
- Responsive layout tested

## Future Scope

Possible future additions include real inventory integration, booking/cancellation, staff dashboard, guest authentication, multilingual conversations, human-agent handoff, monitoring, and persistent conversation history.

The current implementation intentionally focuses on a practical and maintainable hotel assistant rather than adding unnecessary infrastructure.

---

## License

This project was created as a take-home assignment and demonstration project.
