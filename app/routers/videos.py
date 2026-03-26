from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form, Response
from sqlmodel import Session
from app.database import get_session
from app.schemas.video import VideoRead, DeleteVideoRequest, UpdateVideoRequest
from app.auth import get_current_user
from app.models.user import User
from app.services.video_service import (
    create_video,
    get_all_videos,
    get_video_by_id,
    update_video,
    delete_videos_by_ids,
    UNSET,
)

router = APIRouter(prefix="/videos", tags=["videos"])


# GET
@router.get("/", response_model=list[VideoRead])
def get_videos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return get_all_videos(session, current_user.id)


@router.get("/{video_id}", response_model=VideoRead)
def get_video(video_id: int, session: Session = Depends(get_session)):
    video = get_video_by_id(session, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


# POST
@router.post("/", response_model=VideoRead)
def upload_video(
    video_file: UploadFile = File(...),
    title: str = Form(...),
    note: str | None = Form(None),
    recorded_on: str | None = Form(None),
    tag_id: int | None = Form(None),
    session: Session = Depends(get_session),
):
    try:
        video = create_video(session, title, note, recorded_on, tag_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return video


# PATCH
@router.patch("/{video_id}", response_model=VideoRead)
def patch_video(
    video_id: int,
    request: UpdateVideoRequest,
    session: Session = Depends(get_session),
):
    if request.remove_tag:
        tag_id = None
    elif request.tag_id is not None:
        tag_id = request.tag_id
    else:
        tag_id = UNSET
    try:
        updated_video = update_video(
            session,
            video_id,
            request.title,
            request.note,
            tag_id,
            request.recorded_on,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not updated_video:
        raise HTTPException(status_code=404, detail="Video not found")
    return updated_video


# DELETE
@router.delete("/")
def delete_videos(request: DeleteVideoRequest, session: Session = Depends(get_session)):
    if len(request.video_ids) == 0:
        raise HTTPException(status_code=400, detail="No videos found to delete")
    deleted = delete_videos_by_ids(session, request.video_ids)
    if not deleted:
        raise HTTPException(status_code=404, detail="One or more videos not found")
    return Response(status_code=204)
