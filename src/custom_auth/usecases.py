import uuid
from datetime import datetime
from typing import Any, Self

from django.db import IntegrityError, transaction

from custom_auth import models, security
from custom_auth.api import serializers
from src import settings as st


class RegisterError(Exception): ...
class UsernameIsBusyError(RegisterError): ...

class LoginError(Exception): ...
class UserNotFoundError(LoginError): ...
class PasswordIsIncorrectError(LoginError): ...

class LogoutError(Exception): ...

class RegisterUser:
    @transaction.atomic
    def execute(self: Self, username: str, password: str) -> serializers.RegisterDto:
        user = models.CustomUser(
            username=username,
        )
        user.set_password(password)
        try:
            user.save()
        except IntegrityError:
            raise UsernameIsBusyError

        access_jwt=security.create_jwt(
            {"user_id": str(user.id), "username": user.username},
            token_type=st.JwtType.ACCESS,
        )
        refresh_jwt=security.create_jwt(
            {"user_id": str(user.id),"username": user.username},
            token_type=st.JwtType.REFRESH,
        )

        return serializers.RegisterDto(
            username=username,
            access_jwt=access_jwt,
            refresh_jwt=refresh_jwt,
        )


class LoginUser:
    @transaction.atomic
    def execute(self: Self, username: str, password: str) -> serializers.LoginDto:
        try:
            user = models.CustomUser.objects.get(username=username)
        except models.CustomUser.DoesNotExist:
            raise UserNotFoundError

        if not user.check_password(password):
            raise PasswordIsIncorrectError

        access_jwt=security.create_jwt(
            {"user_id": str(user.id), "username": user.username},
            token_type=st.JwtType.ACCESS,
        )
        refresh_jwt=security.create_jwt(
            {"user_id": str(user.id),"username": user.username},
            token_type=st.JwtType.REFRESH,
        )

        return serializers.LoginDto(
            access_jwt=access_jwt,
            refresh_jwt=refresh_jwt,
        )


class LogoutUser:
    @transaction.atomic
    def execute(self: Self, refresh_jwt_payload: dict[str, Any]) -> None:
        try:
            user = models.CustomUser.objects.get(id=uuid.UUID(refresh_jwt_payload["user_id"]))
        except models.CustomUser.DoesNotExist:
            raise LogoutError
        token = models.RefreshJwt(
            id=refresh_jwt_payload["jti"],
            user_id=user,
            expire_at=datetime.fromtimestamp(refresh_jwt_payload["exp"]),
        )
        try:
            token.save()
        except IntegrityError:
            raise LogoutError




