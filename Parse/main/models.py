from django.db import models
from .managers import BookmarkManager
from django.utils import timezone

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    order = models.IntegerField()


class Bookmark(models.Model):
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

    objects = BookmarkManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['url'],
                condition=models.Q(time_deleted__isnull=True),
                name='URL_UNIQUE_IF_NOT_DELETED',
            )
        ]

    def delete(self, using=None, keep_parents=False):
        self.time_deleted = timezone.now()
        self.save()
