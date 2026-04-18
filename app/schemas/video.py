from sqlmodel import SQLModel
from app.schemas.tag import TagRead
from app.schemas.base import TimestampReadMixin


class VideoRead(TimestampReadMixin):
    id: int
    asset_identifier: str | None = None
    title: str
    note: str | None = None
    recorded_on: str | None = None
    tag: TagRead | None = None


class DeleteVideoRequest(SQLModel):
    video_ids: list[int]


class UpdateVideoRequest(SQLModel):
    title: str | None = None
    note: str | None = None
    tag_id: int | None = None
    recorded_on: str | None = None
    remove_tag: bool = False


class DraftResponse(SQLModel):
    draft_response: str
