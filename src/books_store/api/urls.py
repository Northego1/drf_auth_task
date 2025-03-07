import rest_framework.routers
from django.urls import path

from books_store.api import viewsets

router = rest_framework.routers.SimpleRouter()
router.register("books", viewsets.BookStoreViewset, basename="books")
router.register("authors", viewsets.AuthorViewset, basename="authors")

# router.urls + [
#     path("books/<int:book_id>/", viewsets.BookStoreViewset.as_view({"get": "get_book_by_id"})),
# ]