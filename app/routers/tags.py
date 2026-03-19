from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/tags", tags=["tags"])


class CreateTagRequest(BaseModel):
    name: str


class DeleteTagRequest(BaseModel):
    tag_ids: list[int]


# GET
@router.get("/")
def get_tags():
    return {"data": "all tags"}


# POST
@router.post("/")
def create_tag(request: CreateTagRequest):
    return {"created_tag": request.name}


# PATCH
@router.patch("/{tag_id}")
def update_tag(tag_id: int, name: str):
    return {"tag_id": tag_id, "updated_name": name}


# DELETE
@router.delete("/")
def delete_custom_tag(request: DeleteTagRequest):
    return {"deleted_tag_ids": request.tag_ids}
