from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Tuple

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from main_app.models import User
from django.shortcuts import get_object_or_404
from ninja import Router, Schema, errors
from ninja.schema import validator
from ninja.security import HttpBearer

from main_app.models import AuthToken

ALGORITHM = "HS256"
access_token_jwt_subject = "access"

router = Router()


class LoginInput(Schema):
    username: str
    password: str


class RefreshTokenInput(Schema):
    refresh_token: str


class TokenResponse(Schema):
    refresh_token: str
    access_token: str


class TokenPayload(Schema):
    user_id: int = None
    exp: int = None


def create_access_token(*, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_auth_token(user: User):
    token, _ = AuthToken.objects.get_or_create(user=user)
    return {
        "refresh_token": token.key,
        "access_token": create_access_token(data={"user_id": user.id}),
    }


def authenticate_and_create_token(username: str, password: str) -> Tuple[Dict, bool]:

    user = authenticate(username=username, password=password)

    if user:
        return create_auth_token(user), True

    return None, False


@router.post("/login", response=TokenResponse, auth=None)
def login_api(request, input: LoginInput):
    token, succeed = authenticate_and_create_token(
        username=input.username, password=input.password
    )
    if succeed:
        return token
    else:
        raise errors.HttpError(status_code=401, message="Unauthorized")


@router.post("/refresh-token", response=TokenResponse, auth=None)
def refresh_token_api(request, input: RefreshTokenInput):
    try:
        token_obj = AuthToken.objects.get(key__iexact=input.refresh_token)
        return {
            "refresh_token": token_obj.key,
            "access_token": create_access_token(
                data={"user_id": token_obj.user.id}
            )
        }
    except AuthToken.DoesNotExist:
        raise errors.HttpError(status_code=401, message="Unauthorized")
    except AuthToken.MultipleObjectsReturned:
        raise errors.HttpError(status_code=401, message="Unauthorized")


def get_time_from_int(value: int) -> datetime:
    """
    :param value: seconds since the Epoch
    :return: datetime
    """
    if not isinstance(value, int):  # pragma: no cover
        raise TypeError("an int is required")
    return datetime.fromtimestamp(value, timezone.utc)


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
            token_data = TokenPayload(**payload)
        except:  # noqa
            return None

        return get_object_or_404(User, id=token_data.user_id)
