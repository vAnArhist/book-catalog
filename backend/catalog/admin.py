from django.contrib import admin
from .models import Book, Tag, Author, BookImage


class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("Title", "ISBN", "Year", "UpdatedAt")
    search_fields = ("Title", "ISBN", "Authors__Name", "Tags__Name")
    list_filter = ("Year", "Tags")  # ✅ без Tags__Type
    autocomplete_fields = ("Authors", "Tags")  # ✅ автодоповнення
    inlines = [BookImageInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("Name", "Slug")  # ✅ без Type
    search_fields = ("Name", "Slug")        # ✅ потрібно для autocomplete
    # list_filter прибрали повністю, бо Type більше нема


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ("Name",)


@admin.register(BookImage)
class BookImageAdmin(admin.ModelAdmin):
    list_display = ("Book", "Kind", "CreatedAt")
    list_filter = ("Kind",)
