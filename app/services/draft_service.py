import anthropic
from anthropic.types import TextBlock
import os
from dotenv import load_dotenv
from app.models.user_stats import UserStats
from app.models.enums import GenderEnum, UnitEnum
from datetime import date
from app.models.video import Video

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


def generate_draft(video: Video, stats: UserStats, user_prompt: str) -> str:
    stats_line = format_stats_line(stats)
    lift = video.tag.name if video.tag else "Unknown lift"
    prompt = f"""You are helping a user write a post for r/formcheck on Reddit. If the lift is unknown, attempt to infer from the video title or user_prompt variable.
    User stats: {stats_line}
    Lift: {lift}
    Video title: {video.title}
    User notes: {video.note or 'None'}
    User concern: {user_prompt}
    Write a concise r/formcheck post including the stats line, lift info, and their specific question. Keep it under 200 words."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    content = message.content[0]
    if not isinstance(content, TextBlock):
        raise ValueError("Expected content to be a TextBlock")
    return content.text
