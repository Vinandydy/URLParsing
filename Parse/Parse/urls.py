from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from main.views import MainApiView, FavoriteViewSet

router = routers.SimpleRouter()
router.register(r'url', MainApiView, basename='main')
router.register(r'favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='obtain'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh')
]

urlpatterns += router.urls
