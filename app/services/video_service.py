from sqlmodel import Session, select
from app.models.video import Video
from datetime import datetime, timezone


def get_all_videos(session: Session):
    return session.exec(select(Video)).all()


def get_video_by_id(session: Session, video_id: int):
    return session.get(Video, video_id)


def create_video(
    session: Session, title: str, note: str | None, recorded_on: str | None
):
    new_video = Video(title=title, note=note, recorded_on=recorded_on)
    session.add(new_video)
    session.commit()
    session.refresh(new_video)
    return new_video


def update_video(
    session: Session,
    video_id: int,
    title: str | None,
    note: str | None,
    recorded_on: str | None,
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
    video.updated_on = datetime.now(timezone.utc)
    session.commit()
    session.refresh(video)
    return video


def delete_video(session: Session, video_id: int):
    video = session.get(Video, video_id)
    if not video:
        return False
    session.delete(video)
    session.commit()
    return True
