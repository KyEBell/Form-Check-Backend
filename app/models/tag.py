from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.video import Video


class Tag(TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    videos: list["Video"] = Relationship(back_populates="tag")
