from http.client import responses

from django.shortcuts import render
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import action, permission_classes

from .serializers import *
from .services import partial, CustomPagination, xlsx_format
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

    #Тут интересно почему в скобках все пишут, не очень понятен момент
    def get_permissions(self):
        if self.action == "destroy":
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'create':
            return MainPostSerializer
        elif self.action in ['retrieve', 'destroy']:
            return MainDetailSerializer
        return MainSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['post'],
        url_path='xlsx',
        permission_classes = [AllowAny]
    )
    def to_xlsx(self, _):
        data = self.get_queryset()
        response = xlsx_format(data)
        return response


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    queryset = Favorite.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return FavoriteCreateSerializer
        return FavoriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
