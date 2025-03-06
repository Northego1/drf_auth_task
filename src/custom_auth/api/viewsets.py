from typing import Self

from rest_framework import (
    decorators,
    exceptions,
    request,
    response,
    status,
    viewsets,
)

from custom_auth import models, usecases
from custom_auth.api import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

    @decorators.action(
        methods=["POST"],
        detail=False,
        serializer_class=serializers.UserSerializer,
    )
    def register(self, request: request.Request) -> None:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        usecase = usecases.RegisterUser()
        try:
            register_dto = usecase.execute(username=username, password=password)
        except usecases.RegisterError:
            raise exceptions.ValidationError(
                detail="User already exists",
            )
        return response.Response(
            data=register_dto.to_dict(),
            status=status.HTTP_201_CREATED,
        )


