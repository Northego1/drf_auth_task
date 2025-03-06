import json
from dataclasses import asdict, dataclass
from typing import Self

from rest_framework import serializers

import custom_auth.models


@dataclass(slots=True, frozen=True)
class RegisterDto:
    username: str
    access_jwt: str
    refresh_jwt: str

    def json(self: Self) -> str:
        return json.dumps(asdict(self))

    def to_dict(self: Self) -> dict:
        return asdict(self)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = custom_auth.models.CustomUser
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}
