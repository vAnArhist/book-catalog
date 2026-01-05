from django.db import models
# from django.utils.text import slugify
from slugify import slugify


class Tag(models.Model):
    Name = models.CharField(max_length=80, unique=True)
    Slug = models.SlugField(max_length=100, unique=True, db_index=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate slug only if empty -> stable URLs even if Name changes later
        if not self.Slug:
            base = slugify(self.Name)
            if not base:
                base = "tag"  # fallback if Name becomes empty after normalization

            candidate = base
            i = 2

            # Ensure uniqueness (handle collisions after transliteration)
            while Tag.objects.filter(Slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{i}"
                i += 1

            self.Slug = candidate

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.Name}"


class Author(models.Model):
    Name = models.CharField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.Name


class Book(models.Model):
    Title = models.CharField(max_length=255, db_index=True)
    Description = models.TextField(blank=True)
    Language = models.CharField(max_length=32, blank=True)
    Year = models.PositiveIntegerField(null=True, blank=True)
    ISBN = models.CharField(max_length=32, blank=True, db_index=True)

    Authors = models.ManyToManyField(Author, blank=True, related_name="Books")
    Tags = models.ManyToManyField(Tag, blank=True, related_name="Books")

    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.Title


class BookImage(models.Model):
    class ImageKind(models.TextChoices):
        COVER = "cover", "Cover"
        SCAN = "scan", "Scan"

    Book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="Images")
    Kind = models.CharField(max_length=16, choices=ImageKind.choices)
    Image = models.ImageField(upload_to="books/%Y/%m/")
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.Book.Title} [{self.Kind}]"
