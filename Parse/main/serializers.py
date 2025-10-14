from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from main.models import Bookmark, RecipeBookmark, VideoBookmark, ArticleBookmark
from main.services import partial


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleBookmark
        fields = ['favicon', 'title', 'url', 'description', 'theme', 'length', 'published']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoBookmark
        fields = ['favicon', 'title', 'url', 'description', 'duration', 'hosting', 'author', 'preview']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeBookmark
        fields = ['favicon', 'title', 'url', 'description', 'category', 'difficult', 'duration']


class BookmarkMapping(PolymorphicSerializer):
    model_serializer_mapping = {
        VideoBookmark: VideoSerializer,
        ArticleBookmark: ArticleSerializer,
        RecipeBookmark: RecipeSerializer
    }