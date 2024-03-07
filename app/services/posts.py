import boto3

from app.config import settings
from app.schemas.posts import PostSchemaDTO, PostSchemaViewModel


def get_dynamodb():
    return boto3.resource(
        "dynamodb",
        aws_access_key_id=settings.ACCESS_KEY,
        aws_secret_access_key=settings.SECRET_ACCESS_KEY,
    )


async def save_post(post: PostSchemaDTO):
    table = get_dynamodb().Table("posts")
    response = table.get_item(Key={'user_uuid': post.user_uuid})

    if "Item" in response:
        current_posts = response["Item"].get("posts", [])
    else:
        current_posts = []

    current_posts.append(post.text)
    table.update_item(
        Key={"user_uuid": post.user_uuid},
        UpdateExpression="SET posts = :val",
        ExpressionAttributeValues={":val": current_posts}
    )


async def get_posts(user_uuid: str) -> PostSchemaViewModel:
    table = get_dynamodb().Table("posts")
    response = table.get_item(Key={"user_uuid": user_uuid})

    if "Item" in response and "posts" in response["Item"]:
        return PostSchemaViewModel(posts=response["Item"]["posts"])
    else:
        return []

