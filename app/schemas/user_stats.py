from sqlmodel import SQLModel
from app.schemas.base import TimestampReadMixin
from app.models.enums import UnitEnum
from typing import Optional


class UserStatsRead(TimestampReadMixin):
    height: Optional[int] = None
    weight: Optional[float] = None
    unit: UnitEnum
    years_lifting: Optional[int] = None
    squat_1rm: Optional[int] = None
    bench_press_1rm: Optional[int] = None
    deadlift_1rm: Optional[int] = None
    overhead_press_1rm: Optional[int] = None
    barbell_row_1rm: Optional[int] = None


class UpdateUserStatsRequest(SQLModel):
    height: Optional[int] = None
    weight: Optional[float] = None
    unit: Optional[UnitEnum] = None
    years_lifting: Optional[int] = None
    squat_1rm: Optional[int] = None
    bench_press_1rm: Optional[int] = None
    deadlift_1rm: Optional[int] = None
    overhead_press_1rm: Optional[int] = None
    barbell_row_1rm: Optional[int] = None
