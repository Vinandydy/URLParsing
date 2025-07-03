import django_filters

from .models import Bookmark


#Возможно с логикой переборщил или можно что-то убрать, но решил явно обозначить как фильтровать
class BookmarkFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='contains')
    url = django_filters.CharFilter(field_name='url', lookup_expr='contains')
    time_created = django_filters.DateFilter(field_name='time_created', lookup_expr='gte')

    class Meta:
        model = Bookmark
        fields = ['title', 'url', 'time_created']