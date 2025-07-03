from django.shortcuts import render

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from .serializers import *
from .services import Partial, CustomPagination
# Create your views here.



class MainApiView(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    pagination_class = CustomPagination
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