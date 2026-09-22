# Sunrise Hotel Guest Assistant

An AI-powered hotel guest assistant that helps guests get information about Sunrise Hotel and check room availability through a simple conversational web interface.

## Live Demo

🌐 **Frontend:**
https://sunrise-hotel-co65.vercel.app/

🔗 **Backend:**
https://sunrise-hotel-ten.vercel.app/

> The frontend is deployed on Vercel and the FastAPI backend is deployed separately. The frontend communicates with the backend through the `/health` and `/api/chat` endpoints.

---

# Overview

Sunrise Hotel Guest Assistant is a full-stack AI application designed to help hotel guests quickly find information about:

- Hotel amenities
- Rooms and room features
- Breakfast
- Check-in and check-out
- Hotel policies
- Hotel services
- Room suitability
- Room availability

The application combines an LLM for natural-language understanding and tool selection with deterministic Python business logic for hotel information and availability.

The main design principle is:

> **Use AI for understanding and conversation, but keep business-critical decisions deterministic.**

---

# Customer Problem

Hotel guests frequently have questions about rooms, amenities, policies, breakfast, and availability.

Instead of requiring guests to navigate through multiple hotel pages or wait for hotel staff, the assistant provides a conversational interface where guests can ask questions naturally.

For example:

```text
What time is check-in?

Does the hotel have a swimming pool?

Which room is suitable for three guests?

Is breakfast included in the Deluxe Room?

Do you have rooms available from October 10 to October 12 for 3 guests?
```

The goal is to provide quick, useful answers while preventing the AI from inventing hotel information.

---

# Guest Journey

```text
Guest opens the application
        ↓
Frontend checks backend health
        ↓
Guest asks a question
        ↓
Next.js sends question + conversation context
        ↓
FastAPI receives the request
        ↓
LLM understands the guest's intent
        ↓
LLM selects an appropriate tool
        ↓
Python backend executes the tool
        ↓
Tool retrieves authoritative hotel data
        ↓
LLM generates a natural-language response
        ↓
Frontend displays the response
```

For availability requests:

```text
Guest asks about availability
        ↓
LLM identifies availability intent
        ↓
Availability tool is called
        ↓
Python validates dates and guest count
        ↓
Python checks room inventory
        ↓
Structured availability result
        ↓
Backend formats the result
        ↓
Frontend displays available room cards
```

The LLM does **not** determine whether a room is actually available.

---

# Features

## Conversational Hotel Assistant

Guests can ask natural-language questions about the hotel.

Examples:

```text
What time is check-in?

Does the hotel have a swimming pool?

What restaurants are available?

What is the cancellation policy?

Is breakfast included in the Deluxe Room?
```

---

## Room Information

The assistant can provide information about:

- Room types
- Maximum guests
- Beds
- Room size
- Price
- Breakfast inclusion
- Room features

---

## Room Suitability

Guests can ask questions such as:

```text
Which room can accommodate 3 guests?
```

The backend determines suitable rooms based on their configured guest capacity.

---

## Room Availability

Guests can ask for availability for a specific:

- Check-in date
- Check-out date
- Number of guests

Example:

```text
Do you have a room available from October 10 to October 12 for 3 guests?
```

The backend checks the mock room inventory and returns rooms available for the complete requested stay.

Availability results are displayed using structured room cards in the frontend.

---

## Conversation Context

The assistant supports follow-up questions.

Example:

```text
User:
Do you have rooms available from October 10 to October 12 for 3 guests?

Assistant:
Yes, several rooms are available...

User:
What about breakfast?

Assistant:
The available rooms include breakfast...
```

The previous conversation is sent to the backend so the assistant can understand follow-up questions.

---

## Loading States

The frontend displays a loading indicator while waiting for the assistant response.

---

## Backend Connection State

When the application first loads, the frontend checks the backend health endpoint.

```text
Connecting to Sunrise Hotel Assistant...
        ↓
Backend wakes up
        ↓
Health check succeeds
        ↓
Chat becomes available
```

This is particularly useful when the deployed backend is running on infrastructure that may temporarily sleep when idle.

---

## Error Handling

The application handles:

- Backend connection failures
- API failures
- AI/model failures
- Invalid requests
- Unsupported hotel information

The frontend displays user-friendly error messages rather than exposing internal server details.

---

## Responsive Design

The application is designed for:

- Desktop
- Tablet
- Mobile

The chat conversation has an independent scroll area while the header and input remain accessible.

---

# Technology Stack

## Frontend

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS 4
- Lucide React
- React Markdown
- Remark GFM

## Backend

- Python
- FastAPI
- Pydantic
- Pytest

## AI

- Groq API
- `openai/gpt-oss-120b`

## Data

The hotel knowledge base is stored as JSON files:

```text
backend/app/data/
├── hotel.json
├── rooms.json
└── availability.json
```

---

# Architecture

```text
                    ┌──────────────────────┐
                    │        Guest         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Next.js Frontend   │
                    │                      │
                    │  Chat UI             │
                    │  Loading States      │
                    │  Error States        │
                    │  Room Cards          │
                    └──────────┬───────────┘
                               │
                         HTTP / JSON
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    │                      │
                    │  Chat API            │
                    │  Validation          │
                    │  Conversation        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Groq LLM        │
                    │                      │
                    │ Intent Understanding │
                    │ Tool Selection       │
                    │ Response Generation  │
                    └──────────┬───────────┘
                               │
                         Tool Calls
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Python Tools     │
                    │                      │
                    │ hotel_info()         │
                    │ room_info()          │
                    │ suitable_rooms()     │
                    │ availability()       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      JSON Data       │
                    │                      │
                    │ Hotel Information     │
                    │ Room Information      │
                    │ Availability         │
                    └──────────────────────┘
```

---

# AI and Tool Calling

The LLM is responsible for:

- Understanding natural-language guest questions
- Identifying the user's intent
- Selecting the appropriate tool
- Understanding conversation context
- Generating natural-language responses

The LLM is **not** responsible for:

- Directly accessing the database or files
- Deciding room inventory
- Determining room availability
- Making business-critical availability decisions
- Inventing hotel information

The backend exposes four tools:

```text
hotel_info()
room_info(room_name)
suitable_rooms(guests)
availability(check_in, check_out, guests)
```

The Python backend executes the selected tool and supplies its result to the application.

---

# Why Use AI?

Natural-language hotel questions can be expressed in many different ways.

For example:

```text
Do you have anything for three people?

Which room works for 3 guests?

We are a group of three. What can we book?
```

These questions have the same underlying intent.

An LLM is useful for understanding this natural language and selecting the appropriate tool.

However, once the required data has been identified, deterministic backend logic is used wherever possible.

---

# Deterministic Availability Logic

Availability is intentionally handled outside the LLM.

For example:

```text
Check-in: 2026-10-10
Check-out: 2026-10-12
Guests: 3
```

The backend:

1. Validates the dates.
2. Generates every night in the requested stay.
3. Filters rooms based on maximum guest capacity.
4. Checks inventory for every requested night.
5. Returns only rooms available for the complete stay.

If a room is available on October 10 but unavailable on October 11, it is not returned as available for an October 10–12 stay.

This makes availability deterministic and prevents the model from guessing.

---

# Hallucination Prevention

Hotel information is treated as authoritative data.

The assistant is instructed to:

- Use tools whenever hotel data is required.
- Never invent hotel amenities.
- Never invent room features.
- Never invent prices.
- Never invent hotel policies.
- Never invent services.
- Never invent availability.
- Never contradict tool results.
- Use room-specific tools for room-specific questions.
- Use the availability tool for availability requests.
- Avoid assuming that missing information means something is unavailable.

For example, if the hotel knowledge base contains no information about a helicopter service, the assistant should say that it does not have information about that service instead of claiming that the hotel does not provide it.

This distinction helps prevent unsupported claims.

---

# Handling Missing Information

The system distinguishes between:

```text
Known false
```

and:

```text
Information not available
```

For example, the hotel data explicitly contains:

```text
Airport shuttle:
available = false
```

The assistant can therefore state that an airport shuttle is not available.

However, if the hotel data contains no information about helicopter services, the assistant should respond that it does not have information about the service instead of assuming it is unavailable.

---

# Error and Failure Handling

## Frontend Failure

If the frontend cannot connect to the backend:

```text
Unable to connect to the hotel assistant.
Please try again.
```

The chat input remains disabled until the backend becomes available.

---

## Backend API Failure

If a chat request fails, the frontend displays a user-friendly error message.

Internal server errors are not exposed to the guest.

---

## LLM Failure

If the AI service fails while processing a request, the backend handles the exception and returns an appropriate error response.

---

## Invalid Availability Request

The backend validates:

- Check-in date
- Check-out date
- Guest count

Invalid values are rejected before availability logic is executed.

---

# Backend API

## Health Check

```http
GET /health
```

Example:

```bash
curl https://https://sunrise-hotel-ten.vercel.app/health
```

Response:

```json
{
  "status": "ok"
}
```

---

## Chat

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
curl -X POST https://https://sunrise-hotel-ten.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What time is check-in?",
    "conversation": []
  }'
```

Example response:

```json
{
  "message": "Check-in at Sunrise Hotel is at 2:00 PM.",
  "type": "answer",
  "data": null
}
```

---

## Availability Response

Availability responses use structured data:

```json
{
  "message": "Here are the rooms available for your stay.",
  "type": "availability",
  "data": {
    "available": true,
    "check_in": "2026-10-10",
    "check_out": "2026-10-12",
    "guests": 3,
    "rooms": []
  }
}
```

The frontend uses this structured data to render room cards.

This avoids relying on the LLM to format or reinterpret inventory information.

---

# Project Structure

```text
hotel/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   └── chat.py
│   │   │
│   │   ├── data/
│   │   │   ├── hotel.json
│   │   │   ├── rooms.json
│   │   │   └── availability.json
│   │   │
│   │   ├── schemas/
│   │   │   └── chat.py
│   │   │
│   │   ├── services/
│   │   │   ├── availability_service.py
│   │   │   ├── chat_service.py
│   │   │   ├── hotel_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── room_service.py
│   │   │   └── tools.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── test_availability.py
│   │   ├── test_chat_api.py
│   │   ├── test_edge_cases.py
│   │   ├── test_llm.py
│   │   └── test_room_service.py
│   │
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   │
│   ├── components/
│   │   ├── brand/
│   │   │   └── SunriseLogo.tsx
│   │   │
│   │   └── chat/
│   │       ├── Chat.tsx
│   │       ├── ChatInput.tsx
│   │       ├── MessageBubble.tsx
│   │       ├── RoomCard.tsx
│   │       └── SuggestedQuestions.tsx
│   │
│   ├── lib/
│   │   └── api.ts
│   │
│   ├── types/
│   │   └── chat.ts
│   │
│   ├── public/
│   │   └── logo.svg
│   │
│   ├── .env.example
│   └── package.json
│
└── README.md
```

---

# Local Development

## Prerequisites

Make sure the following are installed:

- Python 3.11+
- Node.js
- npm
- Groq API key

---

# Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

# Frontend Setup

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:3000
```

---

# Environment Variables

## Backend

Create:

```text
backend/.env
```

Example:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

A safe template is included in:

```text
backend/.env.example
```

---

## Frontend

Create:

```text
frontend/.env.local
```

For local development:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

A safe template is included in:

```text
frontend/.env.example
```

The frontend environment variable contains only the backend URL and does not contain secrets.

The Groq API key is kept exclusively on the backend.

---

# Testing

The backend includes automated tests for important hotel, availability, API, edge-case, and LLM flows.

Run:

```bash
python -m pytest -q
```

Current result:

```text
19 passed, 2 warnings
```

The two warnings are dependency deprecation warnings from the FastAPI/Starlette test client and do not represent test failures.

---

# Frontend Production Build

The production build has also been verified successfully.

Run:

```bash
npm run build
```

Current result:

```text
✓ Compiled successfully
✓ Finished TypeScript
✓ Generating static pages
✓ Finalizing page optimization
```

---

# Evaluation Scenarios

The application was evaluated against the following scenarios.

| #  | Scenario                                                 | Expected Behavior                                     |
| -- | --------------------------------------------------------- | ------------------------------------------------------- |
| 1  | Ask for check-in time                                    | Returns the hotel's check-in time                      |
| 2  | Ask about hotel amenities                                | Retrieves information from the hotel knowledge base    |
| 3  | Ask whether breakfast is included in a specific room     | Uses room-specific information                         |
| 4  | Ask which room supports 3 guests                         | Returns suitable rooms                                 |
| 5  | Check availability for valid dates and guests            | Calls the availability tool and returns room cards     |
| 6  | Ask a follow-up question about availability              | Uses conversation context                              |
| 7  | Request availability outside the mock calendar           | Clearly states that availability data is unavailable   |
| 8  | Ask about information not present in the knowledge base  | Does not invent an answer                               |
| 9  | Submit an invalid or incomplete availability request     | Handles missing/invalid information                    |
| 10 | Backend/API dependency failure                           | Displays a useful frontend error state                 |

---

# Product and UX Decisions

## Why a conversational interface?

Hotel guests naturally ask questions using normal language.

For example:

```text
Do you have anything for three people with breakfast?
```

A conversational interface lets the guest express their request naturally without requiring them to navigate through multiple pages.

---

## Why suggested questions?

Suggested questions help new users understand what the assistant can do and provide immediate entry points into the conversation.

Examples include:

```text
What time is check-in?

What amenities does the hotel have?

Is breakfast included in the Deluxe Room?

Do you have rooms for 3 guests?
```

---

## Why structured availability cards?

Availability is more useful when guests can quickly scan:

- Room name
- Maximum guests
- Beds
- Price
- Breakfast inclusion

Instead of relying on plain conversational text, the frontend receives structured availability data and renders it as room cards.

---

# Engineering Decisions

## Why JSON instead of a database?

The assignment requires only a small hotel knowledge base.

JSON provides a simple and maintainable solution for this scope.

It is:

- Easy to inspect
- Easy to modify
- Easy to test
- Easy to deploy

A production implementation could replace these files with a database or hotel/property management system.

---

## Why not use RAG?

The hotel knowledge base is small and structured.

Introducing embeddings, a vector database, and a retrieval pipeline would add complexity without providing significant value for this application.

Deterministic JSON retrieval is sufficient for the current scope.

---

## Why keep availability outside the LLM?

Availability is a business-critical deterministic operation.

The LLM can understand:

```text
Do you have anything for three people from October 10th to 12th?
```

but it should not decide whether a room is available.

Python performs the actual inventory check.

This makes the system more predictable and easier to test.

---

# AI Design

The application separates AI responsibilities from deterministic responsibilities.

## LLM Responsibilities

```text
Natural-language understanding
        ↓
Intent identification
        ↓
Tool selection
        ↓
Natural-language response generation
```

## Python Responsibilities

```text
Data retrieval
        ↓
Validation
        ↓
Room suitability
        ↓
Availability calculation
        ↓
Structured response
```

This separation reduces the risk of the model making unsupported business decisions.

---

# How the System Handles Unsupported Questions

If the user asks something that is not present in the hotel knowledge base, the assistant does not invent an answer.

For example:

```text
Does Sunrise Hotel have helicopter transportation?
```

If this information is not present in the data, the assistant should communicate that it does not have information about the service.

This is preferable to making an unsupported claim.

---

# Measuring Usefulness

If this assistant were deployed in a real hotel environment, useful metrics could include:

- Percentage of questions answered successfully
- Availability lookup completion rate
- Fallback rate
- AI/model failure rate
- Average response latency
- Number of conversations requiring human assistance
- Guest satisfaction feedback
- Frequency of repeated questions
- Percentage of availability requests successfully completed

These metrics could be used to determine whether the assistant actually reduces guest effort.

---

# Production Improvements

Before using this system in a real hotel environment, I would consider:

### Real Availability Integration

Replace the mock JSON availability data with a real hotel/property management system.

### Booking Flow

Allow guests to proceed from availability results into a booking flow with explicit confirmation.

### Authentication

Add authentication for hotel staff and administrative functionality.

### Monitoring

Add structured logs, metrics, tracing, and monitoring for API and model failures.

### Rate Limiting

Protect the API from abuse and excessive model usage.

### Improved AI Evaluation

Add automated evaluation for:

- Factual accuracy
- Tool selection
- Hallucination rate
- Unsupported answers
- Follow-up understanding

### Multilingual Support

Hotels serve international guests, so multilingual support could improve accessibility.

### Human Handoff

Provide a mechanism for escalating complex requests to hotel staff.

---

# Deployment

## Frontend

The frontend is deployed using Vercel.

Live application:

https://sunrise-hotel-co65.vercel.app/

## Backend

The backend is deployed separately as a FastAPI service.

Backend URL:

https://sunrise-hotel-ten.vercel.app/

The frontend uses:

```text
NEXT_PUBLIC_API_URL
```

to communicate with the deployed backend.

---

# Startup Health Check

When the application loads, the frontend automatically calls:

```http
GET /health
```

The purpose is to:

1. Check whether the backend is reachable.
2. Wake the backend if the hosting provider has put it into an idle state.
3. Prevent users from sending chat requests before the backend is ready.
4. Provide a clear connection state to the user.

The flow is:

```text
Open application
       ↓
Connecting to Sunrise Hotel Assistant...
       ↓
GET /health
       ↓
Backend available
       ↓
Chat enabled
```

If the backend cannot be reached:

```text
Unable to connect to the hotel assistant.
Please try again.
```

---

# Security

The Groq API key is never exposed to the frontend.

The architecture is:

```text
Browser
   │
   │ No Groq API key
   ▼
Next.js
   │
   ▼
FastAPI
   │
   │ GROQ_API_KEY
   ▼
Groq API
```

Environment files containing secrets are excluded from Git.

Only `.env.example` files are committed to the repository.

---

# AI Tools Used During Development

AI-assisted development tools were used during implementation for:

- Architecture planning
- Code generation
- Debugging
- Test scenario design
- UI refinement
- Error analysis
- Documentation assistance

Important technical and product decisions were reviewed and validated through implementation, testing, and production builds.

---

# Final Validation

Backend tests:

```text
19 passed
2 warnings
```

Frontend production build:

```text
✓ Compiled successfully
✓ Finished TypeScript
✓ Generating static pages
```

The application has been tested across:

- Hotel information questions
- Room information
- Room suitability
- Availability
- Follow-up questions
- Unsupported information
- Loading states
- Backend connection states
- API error handling
- Responsive layouts

---

# Future Scope

Potential future additions include:

- Real hotel inventory integration
- Real booking and cancellation workflows
- Payment integration
- Staff dashboard
- Guest authentication
- Multilingual conversations
- Voice interaction
- Human agent handoff
- Production monitoring
- Advanced AI evaluation
- Persistent conversation history

These features were intentionally kept outside the current implementation to maintain a focused and maintainable assignment scope.

---

# License

This project was created as a take-home assignment and demonstration project.
