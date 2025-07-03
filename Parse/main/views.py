from django.shortcuts import render
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework import filters

from .serializers import *
from .services import Partial, CustomPagination
from .filters import BookmarkFilter
# Create your views here.



class MainApiView(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    pagination_class = CustomPagination
    filterset_class = BookmarkFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'url']
    queryset = Bookmark.objects.all()



    def get_serializer_class(self):
        if self.action == 'create':
            return MainPostSerializer
        elif self.action in ['retrieve', 'destroy']:
            return MainDetailSerializer
        return MainSerializer


    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        existing = Bookmark.objects.filter(url=url).first()

        if existing:
            serializer = self.get_serializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)

        parsed = Partial(url)

        if 'error' in parsed:
            return Response(status.HTTP_400_BAD_REQUEST)

        new_url = Bookmark(
            url=url,
            title=parsed.get('name'),
            favicon=parsed.get('favicon'),
            description=parsed.get('description')
        )

        new_url.save()

        serializer = self.get_serializer(new_url)
        return Response(serializer.data, status.HTTP_201_CREATED)


