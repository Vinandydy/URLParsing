from http.client import responses

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd

from rest_framework import mixins, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import action, permission_classes

from .serializers import *
from .services import partial, xlsx_format
from .filters import BookmarkFilter
from .permissions import CustomPermission, AdminOwnerPermission
from .managers import BookmarkManager
# Create your views here.


class MainApiView(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    pagination_class = PageNumberPagination
    filterset_class = BookmarkFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'url']
    queryset = Bookmark.objects.filter(time_deleted__isnull=True)

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

    def get_queryset(self):
        user = self.request.user
        data = Favorite.objects.filter(user__exact=user)
        return data

    def get_permissions(self):
        if self.action == 'destroy':
            return [AdminOwnerPermission()]
        elif self.action == 'create':
            return [CustomPermission()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return FavoriteCreateSerializer
        return FavoriteSerializer

    def destroy(self, request, *args, **kwargs):
        data = self.get_object()
        return Response(status=status.HTTP_204_NO_CONTENT)





