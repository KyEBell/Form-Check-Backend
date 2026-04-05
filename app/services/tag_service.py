from sqlmodel import Session, select
from app.models.tag import Tag
from datetime import datetime, timezone
import uuid


def get_all_tags(session: Session, user_id: uuid.UUID):
    return session.exec(
        select(Tag).where((Tag.user_id == user_id) | (Tag.is_system == True))
    ).all()


def create_custom_tag(session: Session, name: str, user_id: uuid.UUID):
    new_tag = Tag(name=name, user_id=user_id)
    session.add(new_tag)
    session.commit()
    session.refresh(new_tag)
    return new_tag


def update_tag_name(session: Session, tag_id: int, new_name: str, user_id: uuid.UUID):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise ValueError("Tag not found")
    if tag.user_id != user_id:
        raise PermissionError("Not authorized to update this tag")
    if tag.is_system:
        raise PermissionError("Cannot update system tags")
    tag.name = new_name
    tag.updated_on = datetime.now(timezone.utc)
    session.commit()
    session.refresh(tag)
    return tag


def delete_custom_tags(session: Session, tag_ids: list[int], user_id: uuid.UUID):
    tags = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()
    if len(tags) != len(tag_ids):
        return False
    for tag in tags:
        if tag.is_system:
            raise PermissionError("Cannot delete system tags")
        if tag.user_id != user_id:
            raise PermissionError("Not authorized to delete this tag")
        session.delete(tag)
    session.commit()
    return True
