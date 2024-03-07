from fastapi import APIRouter, Depends
from starlette import status

from app.schemas.posts import PostSchemaDTO, PostSchemaViewModel
from app.services.posts import save_post, get_posts
from app.services.users import get_user

router = APIRouter(prefix="/posts")


@router.post("/", status_code=status.HTTP_200_OK)
async def create_post(text: str, user_uuid=Depends(get_user)):
    data = PostSchemaDTO(text=text, user_uuid=user_uuid)
    await save_post(data)


@router.get("/", status_code=status.HTTP_200_OK, response_model=PostSchemaViewModel)
async def retrieve_posts(user_uuid=Depends(get_user)):
    return await get_posts(user_uuid=user_uuid)

