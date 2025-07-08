from django.contrib import admin

from main.models import Bookmark, Favorite

# Register your models here.

admin.site.register(Bookmark)
admin.site.register(Favorite)