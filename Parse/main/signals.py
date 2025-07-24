from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Bookmark, Favorite

@receiver(post_save, sender=Bookmark)
def favorite_signal(sender, instance: Bookmark, created: bool, **kwargs):
    obj = Favorite.objects.filter(bookmark=instance)
    obj.delete()
    print(f"{instance} deleted!")