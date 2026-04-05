from sqlmodel import SQLModel
from app.models.enums import UnitEnum


class LoginRequest(SQLModel):
    email: str
    password: str


class SignupRequest(SQLModel):
    email: str
    username: str
    password: str
    unit: UnitEnum


class LoginResponse(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
