from sqlmodel import SQLModel


class LoginRequest(SQLModel):
    email: str
    password: str


class SignupRequest(SQLModel):
    email: str
    username: str
    password: str


class LoginResponse(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
