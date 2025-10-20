from collections import defaultdict
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.aggregates import ArrayAgg

from django.db import models
from polymorphic.managers import PolymorphicManager


class BookmarkPolymorphicManager(PolymorphicManager):
    def by_type(self):
        queryset = self.get_queryset()
        grouped_ids = queryset.values('content_type').annotate(object_ids=ArrayAgg('object_id'))
        result = {}

        for group in grouped_ids:
            ct_id = group['content_type']
            ids = group['object_ids']
            ct = ContentType.objects.get_for_id(ct_id)
            model = ct.model_class()
            objects = model.objects.filter(pk__in=ids)
            result[ct] = list(objects)

        return result
