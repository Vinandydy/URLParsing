from django.db import models
from .managers import BookmarkManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __str__(self):
        return self.url


class Favorite(models.Model):
    bookmark = models.ForeignKey(
        Bookmark,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='favorite_bookmarks',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные закладки пользователей'
        unique_together = (('bookmark', 'user'),)

@receiver(post_save, sender=Bookmark)
def favorite_signal(sender, instance: Bookmark, created: bool, **kwargs):
    obj = Favorite.objects.filter(bookmark=instance)
    obj.delete()
    print(f"{instance} deleted!")