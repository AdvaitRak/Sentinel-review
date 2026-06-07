# Sentinel

Autonomous code review agent that triggers on every pull request, runs static analysis, executes your test suite in an isolated sandbox, and posts structured feedback before a human reviewer opens the tab.

## Requirements

- Python 3.10+
- Docker (for Phase 4 sandbox)
- ngrok (for local development)

## Setup

1. Clone the repo

   git clone https://github.com/yourname/sentinel.git
   cd sentinel

2. Create and activate a virtual environment

   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate

3. Install dependencies

   pip install -r requirements.txt

4. Set up environment variables

   cp .env.example .env

   Fill in your `.env`:

   GITHUB_TOKEN=ghp_yourtoken
   GITHUB_WEBHOOK_SECRET=your_webhook_secret
   GEMINI_API_KEY=AIza...

## Running locally

Start the server:

   uvicorn main:app --reload

In a separate terminal, start ngrok:

   ngrok http 8000

Copy the ngrok URL (e.g. https://a3f2.ngrok.io) and set your GitHub webhook to:

   https://a3f2.ngrok.io/webhook

## GitHub webhook setup

1. Go to your repo → Settings → Webhooks → Add webhook
2. Payload URL: your ngrok URL + /webhook
3. Content type: application/json
4. Secret: same value as GITHUB_WEBHOOK_SECRET in your .env
5. Events: select "Let me select individual events" → Pull requests only

## Verify it's working

With the server and ngrok running, open a pull request on your repo.
You should see the request logged in your terminal:

   INFO sentinel — Starting review: owner/repo #1

## Project structure

   sentinel/
   ├── main.py                  # FastAPI app
   ├── api/
   │   ├── webhook/
   │   │   ├── router.py        # POST /webhook
   │   │   ├── service.py       # hands off to LangGraph
   │   │   └── schema.py        # request/response models
   │   └── health/
   │       └── router.py        # GET /health
   ├── core/
   │   ├── config.py            # settings from .env
   │   └── security.py          # HMAC signature verification
   └── graph/
       ├── state.py             # PRReviewState
       ├── graph.py             # LangGraph wiring
       └── nodes/
           ├── fetch_pr.py      # Phase 1 — fetch diff
           ├── lint.py          # Phase 2 — ruff
           ├── llm_review.py    # Phase 3 — Gemini
           ├── sandbox.py       # Phase 4 — Docker/pytest
           └── poster.py        # Phase 5 — GitHub comment