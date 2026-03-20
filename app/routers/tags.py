from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from app.database import get_session
from sqlmodel import Session
from app.services.tag_service import (
    get_all_tags,
    create_custom_tag,
    update_tag_name,
    delete_custom_tags,
)

router = APIRouter(prefix="/tags", tags=["tags"])


class CreateTagRequest(BaseModel):
    name: str


class DeleteTagRequest(BaseModel):
    tag_ids: list[int]


# GET
@router.get("/")
def get_tags(session: Session = Depends(get_session)):
    return get_all_tags(session)


# POST
@router.post("/")
def create_tag(request: CreateTagRequest, session: Session = Depends(get_session)):
    return create_custom_tag(session, request.name)


# PATCH
@router.patch("/{tag_id}")
def update_tag(tag_id: int, new_name: str, session: Session = Depends(get_session)):
    updated_tag = update_tag_name(session, tag_id, new_name)
    if not updated_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated_tag


# DELETE
@router.delete("/")
def delete_tag(request: DeleteTagRequest, session: Session = Depends(get_session)):
    if len(request.tag_ids) == 0:
        raise HTTPException(status_code=400, detail="No tags found to delete")
    deleted = delete_custom_tags(session, request.tag_ids)
    if not deleted:
        raise HTTPException(status_code=404, detail="One or more tags not found")
    return Response(status_code=204)
