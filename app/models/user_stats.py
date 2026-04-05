import uuid
from datetime import date
from sqlmodel import Field
from app.models.base import TimestampMixin
from typing import Optional
from app.models.enums import UnitEnum, GenderEnum


class UserStats(TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", unique=True)
    date_of_birth: Optional[date] = None
    height: Optional[int] = None
    weight: Optional[float] = None
    unit: UnitEnum = Field(default=UnitEnum.imperial)
    gender: GenderEnum = Field(default=GenderEnum.prefer_not_to_say)
    years_lifting: Optional[int] = None
    squat_1rm: Optional[int] = None
    bench_press_1rm: Optional[int] = None
    deadlift_1rm: Optional[int] = None
    overhead_press_1rm: Optional[int] = None
    barbell_row_1rm: Optional[int] = None
