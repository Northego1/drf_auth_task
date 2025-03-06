import json
from dataclasses import asdict, dataclass
from typing import Self

from django.db import IntegrityError
from rest_framework import exceptions, serializers

import custom_auth.models
from custom_auth import models, security


@dataclass(slots=True, frozen=True)
class LoginDto:
    access_jwt: str
    refresh_jwt: str

    def json(self: Self) -> str:
        return json.dumps(asdict(self))

    def to_dict(self: Self) -> dict:
        return asdict(self)


@dataclass(slots=True, frozen=True)
class RegisterDto(LoginDto):
    username: str


class RefreshJwtSerializer(serializers.Serializer):
    refresh_jwt = serializers.CharField(required=False, write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        if not request:
            raise exceptions.ValidationError("Request object is missing from context")

        refresh_jwt = request.COOKIES.get("refresh_jwt") or attrs.get("refresh_jwt")

        if not refresh_jwt:
            raise exceptions.ValidationError("Refresh JWT not found")
        refresh_payload = security.decode_and_verify_jwt(refresh_jwt)

        if not refresh_payload:
            raise exceptions.ValidationError("Invalid refresh token")
        try:
            models.RefreshJwt.objects.get(id=refresh_payload["jti"])
        except models.RefreshJwt.DoesNotExist:
            ...
        else:
            raise exceptions.ValidationError("refresh token is invalid")

        return {"refresh_payload": refresh_payload}


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = custom_auth.models.CustomUser
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=128)
    class Meta:
        model = custom_auth.models.CustomUser
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}






