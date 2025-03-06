from typing import Self

from django.db import IntegrityError, transaction

from custom_auth import models, security
from custom_auth.api import serializers


class RegisterError(Exception): ...
class UsernameIsBusyError(RegisterError): ...


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

        return serializers.RegisterDto(
            username=username,
            access_jwt=security.create_jwt(
                {
                    "user_id": user.id,
                    "username": user.username,
                },
                token_type="access",
            ),
            refresh_jwt=security.create_jwt(
                {
                    "user_id": user.id,
                    "username": user.username,
                },
                token_type="refresh",
            ),
        )

