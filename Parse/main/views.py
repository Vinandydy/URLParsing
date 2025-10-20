from django.shortcuts import render
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, AllowAny

from .serializers import *
from .services import partial, CustomPagination
from .filters import BookmarkFilter
from .models import VideoBookmark, ArticleBookmark, RecipeBookmark
# Create your views here.

class VideoBookmarkAPI(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = VideoBookmark.objects.all()
    serializer_class = VideoSerializer

class ArticleBookmarkAPI(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = ArticleBookmark.objects.all()
    serializer_class = ArticleSerializer

class RecipeBookmarkAPI(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = RecipeBookmark.objects.all()
    serializer_class = RecipeSerializer


class ContentCollectionAPI(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    queryset = ContentCollection.objects.all()
    serializer_class = ContentCollectionSerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related('bookmarks__content_object')

