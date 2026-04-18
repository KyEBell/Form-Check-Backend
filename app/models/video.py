from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from app.models.base import TimestampMixin
import uuid

if TYPE_CHECKING:
    from app.models.tag import Tag


class Video(TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    asset_identifier: Optional[str] = None
    user_id: uuid.UUID = Field(foreign_key="user.id")
    title: str
    note: Optional[str] = None
    recorded_on: Optional[str] = None
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id")
    tag: Optional["Tag"] = Relationship(back_populates="videos")
    draft: Optional[str] = None
