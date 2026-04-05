import anthropic
import os
from dotenv import load_dotenv
from app.models.user_stats import UserStats
from app.models.enums import GenderEnum, UnitEnum
from datetime import date

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

gender_display = {
    GenderEnum.male: "M",
    GenderEnum.female: "F",
    GenderEnum.non_binary: "NB",
    GenderEnum.prefer_not_to_say: "?",
}


def calculate_age(dob: date) -> int:
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


def format_stats_line(stats: UserStats) -> str:
    unit = stats.unit if stats.unit else UnitEnum.imperial

    gender = gender_display.get(stats.gender, "?") if stats.gender else "?"

    age = str(calculate_age(stats.date_of_birth)) if stats.date_of_birth else "?"

    weight = (
        f"{stats.weight}{' lbs' if unit == UnitEnum.imperial else ' kg'}"
        if stats.weight
        else "?"
    )

    if stats.height:
        if unit == UnitEnum.imperial:
            feet = stats.height // 12
            inches = stats.height % 12
            height = f"{feet}'{inches}\""
        else:
            height = f"{stats.height} cm"
    else:
        height = "?"
    years = f"{stats.years_lifting} years" if stats.years_lifting else "?"

    return f"{age}{gender} | {weight} | {height} | {years}"
