from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    created_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_on: Optional[datetime] = None
