from app.models.base import TimestampMixin
from sqlmodel import Field
from typing import Optional
import uuid
from app.models.enums import UnitEnum


class UserStats(TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", unique=True)
    height: Optional[int] = None
    weight: Optional[float] = None
    unit: UnitEnum = Field(default=UnitEnum.imperial)
    years_lifting: Optional[int] = None
    squat_1rm: Optional[int] = None
    bench_press_1rm: Optional[int] = None
    deadlift_1rm: Optional[int] = None
    overhead_press_1rm: Optional[int] = None
    barbell_row_1rm: Optional[int] = None
