from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Tuple
from django.core.validators import validate_email
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


class TokenResponse(Schema):
    refresh_token: str
    access_token: str


class LoginInput(Schema):
    username: str
    password: str


@router.post("/login", response=TokenResponse, auth=None)
def login_api(request, input: LoginInput):
    token, succeed = authenticate_and_create_token(
        username=input.username, password=input.password
    )
    if succeed:
        return token
    else:
        raise errors.HttpError(status_code=401, message="Unauthorized")


def register_user(password: str, first_name: str, last_name: str, email: str
) -> Tuple[Optional[User], bool]:
    try:
        user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email
        )

        user.set_password(password)
        user.save()

        return user, True
    except Exception as e:
        return None, False


class RegistrationInput(Schema):
    first_name: str
    last_name: str
    email: str
    password: str

    @validator("email", allow_reuse=True)
    def email_has_correct_format(cls, email):
        try:
            validate_email(email)
            return email
        except Exception:
            raise errors.HttpError(status_code=409, message="Malformed email")

    @validator("password", allow_reuse=True)
    def password_has_minimum_length(cls, password):
        if len(password) < 6:
            raise errors.HttpError(status_code=409, message="Password too small")
        return password


class UserSchema(Schema):
    first_name: str
    last_name: str
    email: str


@router.post("/register", response=UserSchema, auth=None)
def register_api(request, input: RegistrationInput):
    new_user, succeed = register_user(**input.dict())
    print(new_user)
    print(succeed)
    if succeed:
        return new_user

    raise errors.HttpError(status_code=409, message="Username already exists")


class RefreshTokenInput(Schema):
    refresh_token: str


@router.post("/refresh-token", response=TokenResponse, auth=None)
def refresh_token_api(request, input: RefreshTokenInput):
    try:
        token_obj = AuthToken.objects.get(key__iexact=input.refresh_token)
        return {
            "refresh_token": token_obj.key,
            "access_token": create_access_token(data={"user_id": token_obj.user.id}),
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
