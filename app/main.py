from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from contextlib import asynccontextmanager
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: create database and tables
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# add tag to video(s)
class AddTagRequest(BaseModel):
    video_ids: list[int]
    tag_id: int


# Delete videos
class DeleteVideoRequest(BaseModel):
    video_ids: list[int]


# Delete custom tag
class DeleteTagRequest(BaseModel):
    tag_ids: list[int]


# Delete tag(s) from a video
class RemoveTagsFromVideosRequest(BaseModel):
    video_ids: list[int]
    tag_ids: list[int]


# create a custom tag
class CreateTagRequest(BaseModel):
    name: str


# GET
@app.get("/")
def root():
    return {"message": "Form Check Backend Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/videos")
def get_videos(tag: str | None = None):
    if tag:
        return {"data": f"videos filtered by tag: {tag}"}
    return {"data": "all videos"}


@app.get("/videos/{video_id}")
def get_video(video_id: int):
    return {
        "video_id": video_id,
        "title": f"title of video {video_id}",
        "note": f"note of video {video_id}",
        "recorded_at": f"recorded_at of video {video_id}",
        "tags": [f"tag1 of video {video_id}", f"tag2 of video {video_id}"],
    }


@app.get("/tags")
def get_tags():
    return {"data": "all tags"}


# POST
@app.post("/videos")
def upload_video(
    video_file: UploadFile = File(...),
    title: str = Form(...),
    note: str | None = Form(None),
    recorded_at: str | None = Form(None),
):
    return {
        "file_name": video_file.filename,
        "content_type": video_file.content_type,
        "title": title,
        "note": note,
        "recorded_at": recorded_at,
    }


@app.post("/videos/tags")
def add_tag_to_videos(request: AddTagRequest):
    return {"video_ids": request.video_ids, "tag_added": request.tag_id}


@app.post("/tags")
def create_tag(request: CreateTagRequest):
    return {"created_tag": request.name}


# Patch


@app.patch("/videos/{video_id}")
def update_video(
    video_id: int,
    title: str | None = Form(None),
    note: str | None = Form(None),
    recorded_at: str | None = Form(None),
):
    return {
        "video_id": video_id,
        "updated_title": title,
        "updated_note": note,
        "updated_recorded_at": recorded_at,
    }


@app.patch("/videos/{video_id}/tags")
def update_video_tags(video_id: int, tag_ids: list[int] = Form(...)):
    return {"video_id": video_id, "updated_tag_ids": tag_ids}


@app.patch("/tags/{tag_id}")
def update_tag(tag_id: int, name: str = Form(...)):
    return {"tag_id": tag_id, "updated_name": name}


# Delete
@app.delete("/videos")
def delete_videos(request: DeleteVideoRequest):
    return {"deleted_video_ids": request.video_ids}


@app.delete("/videos/tags")
def remove_tags_from_videos(request: RemoveTagsFromVideosRequest):
    return {"video_ids": request.video_ids, "removed_tag_ids": request.tag_ids}


@app.delete("/tags")
def delete_custom_tag(request: DeleteTagRequest):
    return {"deleted_tag_ids": request.tag_ids}
