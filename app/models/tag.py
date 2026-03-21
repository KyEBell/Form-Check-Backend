from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.video import Video


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    created_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_on: Optional[datetime] = None
    videos: list["Video"] = Relationship(back_populates="tag")
