from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


class TimestampMixin(SQLModel):
    created_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_on: Optional[datetime] = None
