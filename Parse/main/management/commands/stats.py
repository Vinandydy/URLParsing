from django.core.management.base import BaseCommand
from main.models import VideoBookmark, ArticleBookmark, RecipeBookmark, Bookmark
from django.db.models import Avg, Sum, Count


class Command(BaseCommand):

    def handle(self, *args, **options):
        total_count = Bookmark.objects.aggregate(Count('id'))['id__count'] or 0
        avg_duration = VideoBookmark.objects.aggregate(Avg('duration'))['duration__avg'] or 0
        total_reading = ArticleBookmark.objects.aggregate(Sum('length'))['length__sum'] or 0

        self.stdout.write(f'Total content: {total_count}')
        self.stdout.write(f'Avg video duration: {avg_duration}')
        self.stdout.write(f'Total reading time: {total_reading}')
