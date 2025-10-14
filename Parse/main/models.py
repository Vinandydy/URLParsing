from django.db import models
from django.utils import timezone
from polymorphic.models import PolymorphicModel
from .managers import BookmarkPolymorphicManager
from polymorphic.managers import PolymorphicManager

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    order = models.IntegerField()


class Bookmark(PolymorphicModel):
    time_created = models.DateTimeField(auto_now_add=True)
    time_deleted = models.DateTimeField(null=True)
    favicon = models.URLField(null=True)
    url = models.URLField(verbose_name='URL')
    title = models.CharField(max_length=255)
    description = models.CharField(null=True, max_length=255)
    group = models.ForeignKey(
        to=Group,
        null=True,
        on_delete=models.SET_NULL,
        related_name='bookmarks',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['url'],
                condition=models.Q(time_deleted__isnull=True),
                name='URL_UNIQUE_IF_NOT_DELETED',
            )
        ]

    objects = PolymorphicManager()

    def delete(self, using=None, keep_parents=False):
        self.time_deleted = timezone.now()
        self.save()


class VideoBookmark(Bookmark):
    platforms = (
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('vk', 'VK'),
        ('other', 'Other')
    )
    duration = models.TimeField()
    hosting = models.CharField(choices=platforms)
    author = models.CharField()
    preview = models.ImageField()


class ArticleBookmark(Bookmark):
    themes = (
        ('it', 'IT'),
        ('money', 'Money'),
        ('history', 'History'),
        ('other', 'Other')
    )
    theme = models.CharField(choices=themes)
    length = models.TimeField()
    published = models.DateField()


class RecipeBookmark(Bookmark):
    categories = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('dessert', 'Dessert'),
        ('other', 'Other')
    )
    difficulties = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    )
    category = models.CharField(choices=categories)
    difficult = models.CharField(choices=difficulties)
    duration = models.TimeField()


class ContentCollection(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024, blank=True)
    items = models.ManyToManyField(Bookmark, related_name='collections')

    class Meta:
        ordering = ['name']
