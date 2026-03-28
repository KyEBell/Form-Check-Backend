from fastapi import APIRouter, Depends, HTTPException
from app.database import get_session
from sqlmodel import Session
from app.schemas.auth import LoginRequest, LoginResponse, SignupRequest
from app.services.auth_service import login_user, signup_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    try:
        data = login_user(request.email, request.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "token_type": "bearer",
    }


@router.post("/signup", response_model=LoginResponse)
def signup(request: SignupRequest, session: Session = Depends(get_session)):
    try:
        data = signup_user(session, request.email, request.password, request.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "access_token": data["access_token"],
        "refresh_token": data["refresh_token"],
        "token_type": "bearer",
    }
