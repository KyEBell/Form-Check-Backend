from sqlmodel import SQLModel
from app.schemas.base import TimestampReadMixin
from app.models.enums import UnitEnum, GenderEnum
from typing import Optional
from datetime import date


class UserStatsRead(TimestampReadMixin):
    date_of_birth: Optional[date] = None
    height: Optional[int] = None
    weight: Optional[float] = None
    unit: UnitEnum
    gender: GenderEnum
    years_lifting: Optional[int] = None
    squat_1rm: Optional[int] = None
    bench_press_1rm: Optional[int] = None
    deadlift_1rm: Optional[int] = None
    overhead_press_1rm: Optional[int] = None
    barbell_row_1rm: Optional[int] = None


class UpdateUserStatsRequest(SQLModel):
    date_of_birth: Optional[date] = None
    height: Optional[int] = None
    weight: Optional[float] = None
    unit: Optional[UnitEnum] = None
    gender: Optional[GenderEnum] = None
    years_lifting: Optional[int] = None
    squat_1rm: Optional[int] = None
    bench_press_1rm: Optional[int] = None
    deadlift_1rm: Optional[int] = None
    overhead_press_1rm: Optional[int] = None
    barbell_row_1rm: Optional[int] = None
