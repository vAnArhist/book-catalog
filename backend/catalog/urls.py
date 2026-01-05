from django.urls import path
from . import views

urlpatterns = [
    path("", views.BookListView, name="book_list"),
    path("book/<int:BookId>/", views.BookDetailView, name="book_detail"),
    path("tag/<slug:TagSlug>/", views.TagDetailView, name="tag_detail"),
]
