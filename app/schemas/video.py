from sqlmodel import SQLModel
from datetime import datetime
from app.schemas.tag import TagRead


class VideoRead(SQLModel):
    id: int
    title: str
    note: str | None = None
    recorded_on: str | None = None
    updated_on: datetime | None = None
    uploaded_on: datetime
    tag: TagRead | None = None


class DeleteVideoRequest(SQLModel):
    video_ids: list[int]


class UpdateVideoRequest(SQLModel):
    title: str | None = None
    note: str | None = None
    tag_id: int | None = None
    recorded_on: str | None = None
    remove_tag: bool = False
