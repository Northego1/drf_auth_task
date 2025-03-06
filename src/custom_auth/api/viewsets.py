from rest_framework import (
    decorators,
    exceptions,
    request,
    response,
    status,
    viewsets,
)

from custom_auth import models, security, usecases
from custom_auth.api import serializers
from src import settings


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserRegisterSerializer

    @decorators.action(
        methods=["POST"],
        detail=False,
        serializer_class=serializers.UserRegisterSerializer,
    )
    def register(self, request: request.Request) -> response.Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        usecase = usecases.RegisterUser()
        try:
            response_dto = usecase.execute(username, password)
        except usecases.RegisterError:
            raise exceptions.ValidationError(
                detail="User already exists",
            )
        resp = response.Response(
            data=response_dto.to_dict(),
            status=status.HTTP_200_OK,
        )
        resp.set_cookie(
            "refresh_jwt",
            response_dto.refresh_jwt,
            max_age=settings.REFRESH_JWT_EXPIRE,
            httponly=True,
        )
        return resp


    @decorators.action(
        methods=["POST"],
        detail=False,
        serializer_class=serializers.UserLoginSerializer,
    )
    def login(self, request: request.Request) -> response.Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        usecase = usecases.LoginUser()

        try:
            response_dto = usecase.execute(username, password)
        except usecases.LoginError:
            raise exceptions.ValidationError(
                detail="Username or password is incorrect",
            )

        resp = response.Response(
            data=response_dto.to_dict(),
            status=status.HTTP_200_OK,
        )
        resp.set_cookie(
            "refresh_jwt",
            response_dto.refresh_jwt,
            max_age=settings.REFRESH_JWT_EXPIRE,
            httponly=True,
        )
        return resp


    @decorators.action(
        methods=["POST"],
        detail=False,
        serializer_class=serializers.RefreshJwtSerializer,
    )
    def refresh(self, request: request.Request) -> response.Response:
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        refresh_payload = serializer.validated_data["refresh_payload"]

        access_jwt = security.create_jwt(
            {
                "user_id": refresh_payload.get("user_id"),
                "username": refresh_payload.get("username"),
            },
            token_type=settings.JwtType.ACCESS,
        )
        return response.Response(
            {
                "access_jwt": access_jwt,
            },
            status=status.HTTP_200_OK,
        )


    @decorators.action(
        methods=["POST"],
        detail=False,
        serializer_class=serializers.RefreshJwtSerializer,
    )
    def logout(self, request: request.Request) -> response.Response:
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        refresh_payload = serializer.validated_data["refresh_payload"]

        usecase = usecases.LogoutUser()

        try:
            usecase.execute(refresh_payload)
        except usecases.LoginError:
            raise exceptions.ValidationError(detail="invalid token")

        return response.Response(status=status.HTTP_204_NO_CONTENT)



