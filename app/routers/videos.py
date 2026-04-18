from fastapi import APIRouter, Depends, HTTPException, Form, Response
from sqlmodel import Session
from app.database import get_session
from app.schemas.video import (
    VideoRead,
    DeleteVideoRequest,
    UpdateVideoRequest,
    DraftResponse,
)
from app.auth import get_current_user
from app.models.user import User
from app.services.video_service import (
    create_video,
    get_all_videos,
    get_video_by_id,
    update_video,
    delete_videos_by_ids,
    save_draft,
    UNSET,
)
from app.services.user_stats_service import get_user_stats
from app.services.draft_service import generate_draft

router = APIRouter(prefix="/videos", tags=["videos"])


# GET
@router.get("/", response_model=list[VideoRead])
def get_videos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    tag_id: int | None = None,
):
    return get_all_videos(session, current_user.id, tag_id)


@router.get("/{video_id}", response_model=VideoRead)
def get_video(
    video_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    video = get_video_by_id(session, video_id, current_user.id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.get("/{video_id}/draft", response_model=DraftResponse)
def get_draft(
    video_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    video = get_video_by_id(session, video_id, current_user.id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if not video.draft:
        raise HTTPException(status_code=404, detail="No draft found for this video")
    return DraftResponse(draft_response=video.draft)


# POST
@router.post("/", response_model=VideoRead)
def upload_video(
    asset_identifier: str | None = Form(None),
    title: str = Form(...),
    note: str | None = Form(None),
    recorded_on: str | None = Form(None),
    tag_id: int | None = Form(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        video = create_video(
            session, asset_identifier, title, note, recorded_on, tag_id, current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return video


@router.post("/{video_id}/draft", response_model=DraftResponse)
def make_draft(
    video_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    video = get_video_by_id(session, video_id, current_user.id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if not video.note or not video.note.strip():
        raise HTTPException(
            status_code=400,
            detail="Please add notes to your video before generating a draft",
        )
    user_stats = get_user_stats(session, current_user.id)
    try:
        draft = generate_draft(video, user_stats)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    save_draft(session, video_id, current_user.id, draft)
    return DraftResponse(draft_response=draft)


# PATCH
@router.patch("/{video_id}", response_model=VideoRead)
def patch_video(
    video_id: int,
    request: UpdateVideoRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
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
            current_user.id,
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
def delete_videos(
    request: DeleteVideoRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if len(request.video_ids) == 0:
        raise HTTPException(status_code=400, detail="No videos found to delete")
    deleted = delete_videos_by_ids(session, request.video_ids, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="One or more videos not found")
    return Response(status_code=204)
