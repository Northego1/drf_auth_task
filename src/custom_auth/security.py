import uuid
from datetime import datetime, timedelta
from time import timezone
from typing import Any

import jwt
from django.utils import timezone

from src import settings as st


def create_jwt(
        payload: dict[str, Any],
        token_type: st.JwtType,
) -> str:
    expire = st.ACCESS_JWT_EXPIRE if token_type == st.JwtType.ACCESS else st.REFRESH_JWT_EXPIRE
    payload.update(
        {
            "jti": str(uuid.uuid4()),
            "type": token_type,
            "exp": (timezone.now() + timedelta(minutes=expire)).timestamp(),
        },
    )
    return jwt.encode(payload=payload, key="SECRET", algorithm="HS256")


def decode_and_verify_jwt(
        token: str,
) -> dict[str, Any] | None:
    """ returns None if token is invalid"""
    try:
        return jwt.decode(token, key="SECRET", algorithms=["HS256"])
    except jwt.exceptions.PyJWTError:
        return None

