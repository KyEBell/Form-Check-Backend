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

    if stats.weight is not None:
        weight_val = (
            int(stats.weight) if stats.weight == int(stats.weight) else stats.weight
        )
        weight = f"{weight_val} {'lbs' if unit == UnitEnum.imperial else 'kg'}"
    else:
        weight = "?"

    if stats.height:
        if unit == UnitEnum.imperial:
            feet = stats.height // 12
            inches = stats.height % 12
            height = f"{feet}'{inches}\""
        else:
            height = f"{stats.height} cm"
    else:
        height = "?"

    years = f"{stats.years_lifting} years of lifting" if stats.years_lifting else "?"

    return f"{age}{gender} | {weight} | {height} | {years}"


def generate_draft(video: Video, stats: UserStats) -> str:
    stats_line = format_stats_line(stats)
    lift = video.tag.name if video.tag else "Unknown lift"

    prompt = f"""You are helping a user write a post for r/formcheck on Reddit.

    Generate ONLY the Reddit post text — no meta-commentary, no instructions, no notes. Ready to paste directly into Reddit.

    Stats line (include exactly as shown): {stats_line}
    Lift: {lift}
    User concern: {video.note or 'No Notes Provided'}

    Format:
        - Line 1: Stats line exactly as provided
        - Line 2: One concise sentence describing what they want checked
        - Line 3: One clear, straightforward question for the community

    Keep it under 75 words. Do not mention the video title. Do not repeat the concern twice. Be direct and simple. Avoid humor, slang or casual quips"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    content = message.content[0]
    if not isinstance(content, TextBlock):
        raise ValueError("Expected content to be a TextBlock")
    return content.text
