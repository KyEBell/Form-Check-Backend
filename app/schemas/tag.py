from sqlmodel import SQLModel
from app.schemas.base import TimestampReadMixin


class TagRead(TimestampReadMixin):
    id: int
    name: str
    is_system: bool


class CreateTagRequest(SQLModel):
    name: str


class UpdateTagRequest(SQLModel):
    name: str


class DeleteTagRequest(SQLModel):
    tag_ids: list[int]
