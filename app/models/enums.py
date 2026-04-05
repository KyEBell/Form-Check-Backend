from enum import Enum


class UnitEnum(str, Enum):
    imperial = "imperial"
    metric = "metric"


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    non_binary = "non_binary"
    prefer_not_to_say = "prefer_not_to_say"
