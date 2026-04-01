from fastapi import APIRouter, Depends, HTTPException, Response
from app.database import get_session
from sqlmodel import Session
from app.auth import get_current_user

from app.models.user import User
from app.schemas.tag import (
    TagRead,
    CreateTagRequest,
    UpdateTagRequest,
    DeleteTagRequest,
)
from app.services.tag_service import (
    get_all_tags,
    create_custom_tag,
    update_tag_name,
    delete_custom_tags,
)

router = APIRouter(prefix="/tags", tags=["tags"])


# GET
@router.get("/", response_model=list[TagRead])
def get_tags(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return get_all_tags(session, current_user.id)


# POST
@router.post("/", response_model=TagRead)
def create_tag(
    request: CreateTagRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_custom_tag(session, request.name, current_user.id)


# PATCH
@router.patch("/{tag_id}", response_model=TagRead)
def update_tag(
    tag_id: int,
    request: UpdateTagRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        updated_tag = update_tag_name(session, tag_id, request.name, current_user.id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Tag not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Not authorized to update this tag")
    return updated_tag


# DELETE
@router.delete("/")
def delete_tag(
    request: DeleteTagRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if len(request.tag_ids) == 0:
        raise HTTPException(status_code=400, detail="No tags found to delete")

    try:
        deleted = delete_custom_tags(session, request.tag_ids, current_user.id)
        if not deleted:
            raise HTTPException(status_code=404, detail="One or more tags not found")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return Response(status_code=204)
