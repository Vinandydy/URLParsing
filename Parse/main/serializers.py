from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main.models import Bookmark, Favorite
from main.services import partial


class MainPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['url']

    def validate(self, attrs):
        url = attrs['url']
        existing = Bookmark.objects.filter(url=url).first()
        if existing:
            raise ValidationError("Такое URL уже существует")
        return url

    def create(self, validated_data):
        url = validated_data['url']

        parsed = partial(url)
        if 'error' in parsed:
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


class FavoriteCreateSerializer(serializers.ModelSerializer):
    bookmark = serializers.PrimaryKeyRelatedField(
        queryset=Bookmark.objects.filter(time_deleted__isnull=True),
        required=False,
        allow_null=False,
        label="Закладка",
    )

    class Meta:
        model = Favorite
        fields = ['bookmark']

    def validate(self, attrs):
        bookmark = attrs['bookmark']
        if bookmark is None:
            raise ValidationError("Нету закладки")
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        bookmark = validated_data['bookmark']
        return Favorite.objects.create(bookmark=bookmark, user=user)


class FavoriteSerializer(serializers.ModelSerializer):

    bookmark = MainSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['bookmark', 'user']

    def list(self, request):
        user = request.user
        return Favorite.objects.filter(user__exact=user)