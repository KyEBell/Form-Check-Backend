from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional


class TimestampReadMixin(SQLModel):
    created_on: datetime
    updated_on: Optional[datetime] = None
