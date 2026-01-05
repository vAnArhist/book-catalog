from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from .models import Book, Tag, BookImage
from django.db.models import Case, When, Value, IntegerField, F
from django.db.models.functions import Upper
from django.db.models import Count


def BookListView(request):
    Query = (request.GET.get("q") or "").strip()
    Mode = request.GET.get("mode") or "and"  # "and" | "or"
    SelectedTagIds = request.GET.getlist("tag")  # ["1","5",...]

    Books = Book.objects.all().prefetch_related("Tags", "Authors", "Images")

    if Query:
        Books = Books.filter(
            Q(Title__icontains=Query) |
            Q(Authors__Name__icontains=Query) |
            Q(ISBN__icontains=Query)
        ).distinct()

    if SelectedTagIds:
        if Mode == "or":
            Books = Books.filter(Tags__id__in=SelectedTagIds).distinct()
        else:
            # AND: книга має містити всі вибрані теги
            Books = (Books
                     .filter(Tags__id__in=SelectedTagIds)
                     .annotate(MatchedTags=Count("Tags", filter=Q(Tags__id__in=SelectedTagIds), distinct=True))
                     .filter(MatchedTags=len(SelectedTagIds))
                     .distinct())
    # CAPSLOCK tags first, then alphabetically
    AllTags = (
        Tag.objects
        .annotate(
            IsCaps=Case(
                When(Name=Upper(F("Name")), then=Value(0)),  # CAPSLOCK → перші
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by("IsCaps", "Name")
    )

    Context = {
        "Books": Books.order_by("-UpdatedAt")[:200],
        "AllTags": AllTags,
        "Query": Query,
        "Mode": Mode,
        "SelectedTagIds": set(map(int, SelectedTagIds)) if SelectedTagIds else set(),
    }

    TagBookCount = dict(
        Tag.objects.annotate(BookCount=Count("Books")).values_list("id", "BookCount")
    )

    Context = {
        "Books": Books.order_by("-UpdatedAt")[:200],
        "AllTags": AllTags,
        "Query": Query,
        "Mode": Mode,
        "SelectedTagIds": set(map(int, SelectedTagIds)) if SelectedTagIds else set(),
        "TagBookCount": TagBookCount,
    }

    return render(request, "catalog/book_list.html", Context)


def BookDetailView(request, BookId: int):
    BookObj = get_object_or_404(Book.objects.prefetch_related("Tags", "Authors", "Images"), id=BookId)

    Cover = BookObj.Images.filter(Kind=BookImage.ImageKind.COVER).first()
    Scans = BookObj.Images.filter(Kind=BookImage.ImageKind.SCAN).order_by("CreatedAt")

    TagIds = list(BookObj.Tags.values_list("id", flat=True))

    Similar = []
    if TagIds:
        Similar = (Book.objects
                   .filter(Tags__id__in=TagIds)
                   .exclude(id=BookObj.id)
                   .annotate(CommonTags=Count("Tags", filter=Q(Tags__id__in=TagIds), distinct=True))
                   .order_by("-CommonTags", "-UpdatedAt")
                   .prefetch_related("Tags", "Authors", "Images")
                   .distinct()[:12])
 
    TagBookCount = dict(
        Tag.objects.annotate(BookCount=Count("Books")).values_list("id", "BookCount")
    )

    Context = {
        "Book": BookObj,
        "Cover": Cover,
        "Scans": Scans,
        "SimilarBooks": Similar,
        "TagBookCount": TagBookCount,
    }
    return render(request, "catalog/book_detail.html", Context)

def TagDetailView(request, TagSlug: str):
    TagObj = get_object_or_404(Tag, Slug=TagSlug)
    Books = (Book.objects
             .filter(Tags=TagObj)
             .prefetch_related("Tags", "Authors", "Images")
             .order_by("-UpdatedAt"))
    return render(request, "catalog/book_list.html", {
        "Books": Books,
        "AllTags": Tag.objects.order_by("Name"),
        "Query": "",
        "Mode": "or",
        "SelectedTagIds": {TagObj.id},
    })