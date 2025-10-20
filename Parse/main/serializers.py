from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from main.models import Bookmark, RecipeBookmark, VideoBookmark, ArticleBookmark, ContentCollection
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


class ContentCollectionSerializer(serializers.ModelSerializer):
    bookmarks_by_type = serializers.SerializerMethodField()

    class Meta:
        model = ContentCollection
        fields = ['id', 'name', 'description', 'bookmarks_by_type']

    def get_by_type(self, obj):
        bookmarks_qs = obj.bookmarks.all()
        grouped = bookmarks_qs.objects.by_type()

        serialized_groups = {}
        for type_name, objects in grouped.items():
            if type_name == 'article':
                serialized_groups[type_name] = ArticleSerializer(objects, many=True).data
            elif type_name == 'video':
                serialized_groups[type_name] = VideoSerializer(objects, many=True).data
            elif type_name == 'recipe':
                serialized_groups[type_name] = RecipeSerializer(objects, many=True).data


        return serialized_groups