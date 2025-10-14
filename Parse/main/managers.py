from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django.db import models
from polymorphic.managers import PolymorphicManager

class BookmarkPolymorphicManager(PolymorphicManager):
    def by_type(self):
        queryset = self.get_queryset()
        group_by = defaultdict(list)
        for obj in queryset:
            content_type = ContentType.objects.get_for_model(obj.content_object)
            group_by[content_type].append(obj.content_object)


