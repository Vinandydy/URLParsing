"""
URL configuration for Parse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from main.views import ArticleBookmarkAPI, VideoBookmarkAPI, RecipeBookmarkAPI

router = routers.SimpleRouter()
router.register(r'video', VideoBookmarkAPI, basename='video')
router.register(r'article', VideoBookmarkAPI, basename='article')
router.register(r'recipe', VideoBookmarkAPI, basename='recipe')

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
