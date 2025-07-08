from django.contrib.auth import get_user_model
from rest_framework import serializers

from main.models import Bookmark, Favorite
from main.services import partial


class MainPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['url']


    def create(self, validated_data):
        url = validated_data['url']

        existing = Bookmark.objects.filter(url=url).first()
        #Тут мне не позволило ошибку передать (мб что-то напутал) (как лучше сделать)
        if existing: return existing

        parsed = partial(url)
        if 'error' in parsed:
            #Попробовал с raise, для получения ошибки, но мне все же кажется, что есть более качественный способ
            raise serializers.ValidationError('Проблема с URL')

        parsed_url = Bookmark.objects.create(
            url = url,
            title = parsed['name'],
            favicon = parsed['favicon'],
            description = parsed['description']
        )

        return parsed_url




class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'favicon']


class MainDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'title', 'description', 'url', 'time_created']

#Тут просит Bookmark сущность, а не URL. Нужно подумать.
class FavoriteCreateSerializer(serializers.ModelSerializer):

    bookmark = serializers.PrimaryKeyRelatedField(
        queryset=Bookmark.objects.all(),
        default=None,
        required=False,
        allow_null=True,
        label="Закладка",
    )
    class Meta:
        model = Favorite
        fields = ['bookmark']

    def create(self, validated_data):
        return Favorite.objects.create(**validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='bookmark.url')
    title = serializers.CharField(source='bookmark.title')

    class Meta:
        model = Favorite
        fields = ['url', 'title']