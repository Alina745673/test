import base64
import hashlib
import hmac

import boto3
from fastapi import HTTPException
from app.config import settings


def get_secret_hash() -> str:
    return base64.b64encode(
        hmac.new(
            bytes(settings.CLIENT_SECRET, "utf-8"),
            bytes("test_user_1" + settings.APP_CLIENT_ID, "utf-8"),
            digestmod=hashlib.sha256
        ).digest()
    ).decode()


def solve_cognito_challenge(client, response: dict):
    auth_response = client.admin_respond_to_auth_challenge(
        ClientId=settings.APP_CLIENT_ID,
        UserPoolId=settings.USER_POOL_ID,
        ChallengeName=response["ChallengeName"],
        Session=response["Session"],
        ChallengeResponses={
            "USERNAME": settings.ADMIN_USER_USERNAME,
            "EMAIL": settings.ADMIN_USER_EMAIL,
            "NEW_PASSWORD": settings.ADMIN_USER_PASSWORD,
            "SECRET_HASH": get_secret_hash(),
        }
    )
    return auth_response


def perform_auth(client) -> dict:
    try:
        response = client.initiate_auth(
            ClientId=settings.APP_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": settings.ADMIN_USER_USERNAME,
                "PASSWORD": settings.ADMIN_USER_PASSWORD,
                "SECRET_HASH": get_secret_hash(),
            }
        )
        if 'ChallengeName' in response:
            auth_response = solve_cognito_challenge(client, response)
            return auth_response
        return response
    except Exception as exc:
        print(exc)      # TODO logger
        raise HTTPException(status_code=401, detail="Unauthorized")


def get_access_token_from_response(response: dict):
    auth_res = response.get('AuthenticationResult')
    if auth_res is None:
        raise ValueError('Authentication failed.')
    return auth_res.get('AccessToken')


def get_user_sub_from_auth_response(client, response: dict):
    access_token = get_access_token_from_response(response)
    user_attrs = client.get_user(
        AccessToken=access_token
    )
    attr_sub = None
    for attr in user_attrs['UserAttributes']:
        if attr['Name'] == 'sub':
            attr_sub = attr['Value']
    return attr_sub


async def get_user():
    try:
        client = boto3.client("cognito-idp", settings.REGION)
        response = perform_auth(client=client)
        sub = get_user_sub_from_auth_response(client, response)

        return sub
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=401, detail="Unauthorized")
