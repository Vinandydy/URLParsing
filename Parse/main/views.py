from django.shortcuts import render
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action, permission_classes

from .serializers import *
from .services import partial, CustomPagination
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
    def to_xlsx(self, request):
        data = self.get_queryset()
        df = pd.DataFrame.from_records(data.values(), exclude=['time_created', 'time_deleted'])
        df.to_excel('data.xlsx', index=False)
        return Response(status=status.HTTP_201_CREATED)