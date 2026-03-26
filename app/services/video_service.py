import uuid

from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.models.video import Video
from datetime import datetime, timezone
from app.models.tag import Tag

UNSET = object()


def get_all_videos(session: Session, user_id: uuid.UUID):
    return session.exec(
        select(Video).where(Video.user_id == user_id).options(selectinload(Video.tag))
    ).all()


def get_video_by_id(session: Session, video_id: int):
    return session.exec(
        select(Video).where(Video.id == video_id).options(selectinload(Video.tag))
    ).first()


def create_video(
    session: Session,
    title: str,
    note: str | None,
    recorded_on: str | None,
    tag_id: int | None,
):
    if tag_id is not None:
        tag = session.get(Tag, tag_id)
        if not tag:
            raise ValueError("Tag not found")
    new_video = Video(
        title=title,
        note=note,
        recorded_on=recorded_on,
        tag_id=tag_id,
    )
    session.add(new_video)
    session.commit()
    session.refresh(new_video)
    return session.exec(
        select(Video).where(Video.id == new_video.id).options(selectinload(Video.tag))
    ).first()


def update_video(
    session: Session,
    video_id: int,
    title: str | None,
    note: str | None,
    tag_id: int | None | object = UNSET,
    recorded_on: str | None = None,
):
    video = session.get(Video, video_id)
    if not video:
        return None
    if title is not None:
        video.title = title
    if note is not None:
        video.note = note
    if recorded_on is not None:
        video.recorded_on = recorded_on
    if tag_id is not UNSET:
        if tag_id is not None:
            tag = session.get(Tag, tag_id)
            if not tag:
                raise ValueError("Tag not found")
        video.tag_id = tag_id
    video.updated_on = datetime.now(timezone.utc)
    session.commit()
    session.refresh(video)
    return session.exec(
        select(Video).where(Video.id == video_id).options(selectinload(Video.tag))
    ).first()


def delete_videos_by_ids(session: Session, video_ids: list[int]):
    videos = session.exec(select(Video).where(Video.id.in_(video_ids))).all()
    if len(videos) != len(video_ids):
        return False
    for video in videos:
        session.delete(video)
    session.commit()
    return True
