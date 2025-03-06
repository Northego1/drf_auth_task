import uuid
from typing import Self

from django.contrib.auth import hashers
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    username = models.CharField(
        max_length=128,
        unique=True,
        null=False,
        db_index=True,
    )
    _password = models.BinaryField(
        null=False,
    )
    USERNAME_FIELD = "username"

    class Meta:
            verbose_name = "User"
            verbose_name_plural = "Users"


    def __str__(self: Self) -> str:
        return f"{self.username}"


    def set_password(self: Self, password: str) -> None: # type: ignore
        self._password = hashers.make_password(password).encode("utf-8")


    def check_password(self: Self, password: str) -> bool: # type: ignore
        return hashers.check_password(password, self._password.decode())



class RefreshJwt(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="refresh_tokens",
        db_index=True,
    )
    expire_at = models.DateField(null=False)




