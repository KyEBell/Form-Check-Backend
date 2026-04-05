import uuid
from sqlmodel import Session, select
from app.models.user_stats import UserStats
from app.schemas.user_stats import UpdateUserStatsRequest
from datetime import datetime, timezone


def get_user_stats(session: Session, user_id: uuid.UUID):
    stats = session.exec(select(UserStats).where(UserStats.user_id == user_id)).first()
    if not stats:
        stats = UserStats(user_id=user_id)
        session.add(stats)
        session.commit()
        session.refresh(stats)
    return stats


def update_user_stats(
    session: Session,
    update_request: UpdateUserStatsRequest,
    user_id: uuid.UUID,
):
    stats = session.exec(select(UserStats).where(UserStats.user_id == user_id)).first()
    if not stats:
        stats = UserStats(user_id=user_id)
        session.add(stats)

    update_data = update_request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(stats, field, value)
    stats.updated_on = datetime.now(timezone.utc)
    session.commit()
    session.refresh(stats)
    return stats
