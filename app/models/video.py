from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.tag import Tag


class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    note: Optional[str] = None
    recorded_on: Optional[str] = None
    updated_on: Optional[datetime] = None
    uploaded_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id")
    tag: Optional["Tag"] = Relationship(back_populates="videos")
