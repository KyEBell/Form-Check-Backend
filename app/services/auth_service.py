import uuid
import httpx
import os
from dotenv import load_dotenv
from sqlmodel import Session
from app.models.user import User

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")


def login_user(email: str, password: str) -> dict:
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    headers = {
        "Content-Type": "application/json",
        "apikey": SUPABASE_ANON_KEY,
    }
    json = {
        "email": email,
        "password": password,
    }
    response = httpx.post(url, json=json, headers=headers)

    if response.status_code != 200:
        error_data = response.json()
        raise ValueError(error_data.get("msg", "Login failed"))
    data = response.json()
    return data


def signup_user(
    session: Session,
    email: str,
    password: str,
    username: str,
) -> dict:
    url = f"{SUPABASE_URL}/auth/v1/signup"
    headers = {
        "Content-Type": "application/json",
        "apikey": SUPABASE_ANON_KEY,
    }
    json = {
        "email": email,
        "password": password,
    }
    response = httpx.post(url, json=json, headers=headers)

    if response.status_code != 200:
        error_data = response.json()
        raise ValueError(error_data.get("msg", "Signup failed"))
    data = response.json()

    user_id = data["user"]["id"]
    new_user = User(id=uuid.UUID(user_id), email=email, username=username)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return data
