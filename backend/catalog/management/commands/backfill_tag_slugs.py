from django.core.management.base import BaseCommand
from catalog.models import Tag


class Command(BaseCommand):
    help = "Generate missing slugs for existing tags."

    def handle(self, *args, **options):
        qs = Tag.objects.filter(Slug="").order_by("id")
        total = qs.count()

        updated = 0
        for t in qs:
            t.save()  # will generate slug by model logic
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Updated {updated}/{total} tags."))
