from sqlmodel import Session, select
from app.models.video import Video


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
