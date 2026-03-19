from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form, Response
from pydantic import BaseModel
from sqlmodel import Session
from app.database import get_session
from app.services.video_service import (
    create_video,
    get_all_videos,
    get_video_by_id,
    update_video,
    delete_video,
)

router = APIRouter(prefix="/videos", tags=["videos"])


class AddTagRequest(BaseModel):
    video_ids: list[int]
    tag_id: int


class DeleteVideoRequest(BaseModel):
    video_ids: list[int]


class RemoveTagsFromVideosRequest(BaseModel):
    video_ids: list[int]
    tag_ids: list[int]


# GET
@router.get("/")
def get_videos(session: Session = Depends(get_session)):
    return get_all_videos(session)


@router.get("/{video_id}")
def get_video(video_id: int, session: Session = Depends(get_session)):
    video = get_video_by_id(session, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


# POST
@router.post("/")
def upload_video(
    video_file: UploadFile = File(...),
    title: str = Form(...),
    note: str | None = Form(None),
    recorded_on: str | None = Form(None),
    session: Session = Depends(get_session),
):
    video = create_video(session, title, note, recorded_on)
    return video


@router.post("/tags")
def add_tag_to_videos(request: AddTagRequest):
    return {"video_ids": request.video_ids, "tag_added": request.tag_id}


# PATCH
@router.patch("/{video_id}")
def patch_video(
    video_id: int,
    title: str | None = Form(None),
    note: str | None = Form(None),
    recorded_on: str | None = Form(None),
    session: Session = Depends(get_session),
):
    updated_video = update_video(session, video_id, title, note, recorded_on)
    if not updated_video:
        raise HTTPException(status_code=404, detail="Video not found")
    return updated_video


@router.patch("/{video_id}/tags")
def update_video_tags(video_id: int, tag_ids: list[int] = Form(...)):
    return {"video_id": video_id, "updated_tag_ids": tag_ids}


# DELETE
@router.delete("/")
def delete_videos(request: DeleteVideoRequest, session: Session = Depends(get_session)):
    deleted_video_ids = []
    for video_id in request.video_ids:
        if delete_video(session, video_id):
            deleted_video_ids.append(video_id)

    if len(deleted_video_ids) == 0:
        raise HTTPException(status_code=404, detail="No videos found to delete")

    return Response(status_code=204)


@router.delete("/tags")
def remove_tags_from_videos(request: RemoveTagsFromVideosRequest):
    return {"video_ids": request.video_ids, "removed_tag_ids": request.tag_ids}
