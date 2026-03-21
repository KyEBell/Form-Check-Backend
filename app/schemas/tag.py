from sqlmodel import SQLModel
from datetime import datetime


class TagRead(SQLModel):
    id: int
    name: str
    created_on: datetime
    updated_on: datetime | None = None


class CreateTagRequest(SQLModel):
    name: str


class UpdateTagRequest(SQLModel):
    name: str


class DeleteTagRequest(SQLModel):
    tag_ids: list[int]
