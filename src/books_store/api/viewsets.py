import django_filters
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    decorators,
    exceptions,
    request,
    response,
    serializers,
    status,
    viewsets,
    pagination
)

from books_store import models
from books_store.api import serializers


class BookFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter(field_name="author")
    class Meta:
        model = models.Book
        fields = ["author"]


class BooksPagination(pagination.PageNumberPagination):
    page_size = 10



class BookStoreViewset(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    pagination_class = BooksPagination

    def create(
            self,
            request: request.Request,
            *args,
            **kwargs,
    ) -> response.Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data["title"]
        author_data = serializer.validated_data["author"]
        count = serializer.validated_data["count"]

        try:
            author = models.Author.objects.get(id=author_data["id"])
        except models.Author.DoesNotExist:
            raise exceptions.APIException("author does not exists")
        book = models.Book(
            title=title,
            author=author,
            count=count,
        )
        try:
            book.save()
        except IntegrityError:
            raise exceptions.APIException("unkown create book error")

        return response.Response(
            {
                "book_title": book.title,
                "author": book.author.id,
            },
            status=status.HTTP_201_CREATED,
        )


    def update(
            self,
            request: request.Request,
            *args,
            **kwargs,
    ) -> response.Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data["title"]
        author_data = serializer.validated_data["author"]
        count = serializer.validated_data["count"]

        try:
            author = models.Author.objects.get(id=author_data["id"])
        except models.Author.DoesNotExist:
            raise exceptions.APIException("author does not exists")
        try:
            book = models.Book.objects.get(id=kwargs["pk"])
        except models.Book.DoesNotExist:
            raise exceptions.APIException("book does not exists")
        book.title = title
        book.author = author
        book.count = count
        try:
            book.save()
        except IntegrityError:
            raise exceptions.APIException("cant put the book")

        return response.Response(
            {
                "book_title": title,
                "author": author.id,
            },
        )


    @decorators.action(
            methods=["POST"],
            detail=True,
    )
    def buy(
            self,
            request: request.Request,
            pk: int,
    ) -> response.Response:
        try:
            book = models.Book.objects.select_for_update().get(id=pk)
        except models.Book.DoesNotExist:
            raise exceptions.APIException("book not found")
        if book.count > 0:
            book.count -= 1
            book.save()
            return response.Response(
                {
                    "book_id": book.id,
                    "book_title": book.title,
                },
                status=status.HTTP_200_OK,
            )
        raise exceptions.APIException("book is out of stock")


class AuthorViewset(viewsets.ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer

    def create(
            self,
            request: request.Request,
            *args,
            **kwargs
    ) -> response.Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]

        author = models.Author(
            first_name=first_name,
            last_name=last_name,
        )

        try:
            author.save()
        except IntegrityError:
            raise exceptions.APIException("unknown author create error")

        author_serializer = serializers.AuthorSerializer(author)
        return response.Response(
            author_serializer.data,
            status=status.HTTP_201_CREATED,
        )


    def update(
            self,
            request: request.Request,
            *args,
            **kwargs,
    ) -> response.Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]

        try:
            author = models.Author.objects.get(id=kwargs["pk"])
        except models.Author.DoesNotExist:
            raise exceptions.APIException("author not found")
        author.id = kwargs["pk"]
        author.first_name = first_name
        author.last_name = last_name
        try:
            author.save()
        except IntegrityError:
            raise exceptions.APIException("cant put the author")

        return response.Response(
            {
                "first_name": first_name,
                "last_name": last_name,
            },
        )
