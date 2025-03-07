from rest_framework import (
    exceptions,
    serializers,
)

from books_store import models


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    first_name = serializers.CharField(max_length=128, required=True)
    last_name = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = models.Author
        fields = ["id", "first_name", "last_name"]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=128, required=True)
    count = serializers.IntegerField(required=True)


    class Meta:
        model = models.Book
        fields = ["id", "title", "author", "count"]

