from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from main.views import MainApiView, FavoriteViewSet

router = routers.SimpleRouter()
router.register(r'url', MainApiView, basename='main')
router.register(r'favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
