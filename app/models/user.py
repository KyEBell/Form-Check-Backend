import uuid
from sqlmodel import Field
from app.models.base import TimestampMixin


class User(TimestampMixin, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
