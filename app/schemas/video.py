from sqlmodel import SQLModel
from app.schemas.tag import TagRead
from app.schemas.base import TimestampReadMixin
from pydantic import field_validator


class VideoRead(TimestampReadMixin):
    id: int
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


class GenerateDraftRequest(SQLModel):
    user_prompt: str

    @field_validator("user_prompt")
    @classmethod
    def prompt_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()


class DraftResponse(SQLModel):
    draft_response: str
