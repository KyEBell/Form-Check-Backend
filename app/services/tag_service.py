from sqlmodel import Session, select
from app.models.tag import Tag
from datetime import datetime, timezone


def get_all_tags(session: Session):
    return session.exec(select(Tag)).all()


def create_custom_tag(session: Session, name: str):
    new_tag = Tag(name=name)
    session.add(new_tag)
    session.commit()
    session.refresh(new_tag)
    return new_tag


def update_tag_name(session: Session, tag_id: int, new_name: str):
    tag = session.get(Tag, tag_id)
    if not tag:
        return None
    tag.name = new_name
    tag.updated_on = datetime.now(timezone.utc)
    session.commit()
    session.refresh(tag)
    return tag


def delete_custom_tags(session: Session, tag_ids: list[int]):
    tags = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()
    if len(tags) != len(tag_ids):
        return False
    for tag in tags:
        session.delete(tag)
    session.commit()
    return True
