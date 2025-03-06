import uuid
from datetime import timedelta
from time import timezone
from typing import Any, Literal

import jwt
from django.utils import timezone


def create_jwt(
        payload: dict[str, Any],
        token_type: Literal["access", "refresh"],
) -> str:
    expire = 5 if token_type == "access" else 60

    payload.update(
        {
            "jti": uuid.uuid4(),
            "type": token_type,
            "exp": timezone.now() + timedelta(minutes=expire),
        },
    )
    return jwt.encode(payload=payload, key="PRIVATE_SECRET", algorithm="HS256")


def decode_and_verify_jwt(
        token: str,
) -> dict[str, Any] | None:
    """ returns None if token is invalid"""
    try:
        return jwt.decode(token, key="PUBLIC_SECRET", algorithms=["HS256"])
    except jwt.exceptions.PyJWTError:
        return None
