from fastapi import APIRouter, Depends
from app.database import get_session
from sqlmodel import Session
from app.auth import get_current_user
from app.models.user import User
from app.schemas.user_stats import UserStatsRead, UpdateUserStatsRequest
from app.services.user_stats_service import get_user_stats, update_user_stats

router = APIRouter(prefix="/user", tags=["users"])


@router.get("/stats", response_model=UserStatsRead)
def get_stats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    stats = get_user_stats(session, current_user.id)
    return stats


@router.patch("/stats", response_model=UserStatsRead)
def update_stats(
    request: UpdateUserStatsRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    stats = update_user_stats(session, request, current_user.id)
    return stats
