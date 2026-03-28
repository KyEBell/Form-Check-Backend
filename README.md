# form-check-backend

FastAPI backend for the Form Check app — a privacy-first gym form check recording app.

## Stack

- Python / FastAPI
- PostgreSQL (local) / Supabase (production)
- SQLModel / SQLAlchemy

## Setup

1. Clone the repo
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file (see `.env.example`)
6. Run: `uvicorn app.main:app --reload`
