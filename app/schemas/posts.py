from datetime import datetime

from pydantic import BaseModel


class PostSchemaDTO(BaseModel):
    user_uuid: str
    text: str
    timestamp: datetime = datetime.now()


class PostSchemaViewModel(BaseModel):
    posts: list[str]
