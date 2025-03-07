from django.db import models


class Author(models.Model):
    id = models.AutoField(
        primary_key=True,
        auto_created=True,
    )
    first_name = models.CharField(
        max_length=128,
        verbose_name="First Name",
    )
    last_name = models.CharField(
        max_length=128,
        verbose_name="Last Name",
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    id = models.AutoField(
        primary_key=True,
        auto_created=True,
    )
    title = models.CharField(
        max_length=128,
        unique=True,
        null=False,
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
    )
    count = models.IntegerField(
        null=False,
    )

    def __str__(self) -> str:
        return self.title

