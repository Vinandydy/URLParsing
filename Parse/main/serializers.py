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

    def validate_url(self, url):
        bookmark = Bookmark.objects.filter(url=url, time_deleted__isnull=True).first()
        if not bookmark:
            raise serializers.ValidationError('Данной URL не существует')
        return url

    def create(self, validated_data):
        request = self.context.get('request')

        user = request.user
        #{'bookmark': <Bookmark: https://pypi.org/project/beautifulsoup4/>}
        url = validated_data['bookmark']
        bookmark = Bookmark.objects.get(url=url, time_deleted__isnull=True)

        if Favorite.objects.filter(bookmark=bookmark, user=user).exists():
            raise serializers.ValidationError('Такая закладка этим пользователем уже добавлена')

        return Favorite.objects.create(bookmark=bookmark, user=user)


class FavoriteSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='bookmark.url')
    title = serializers.CharField(source='bookmark.title')
    favicon = serializers.URLField(source='bookmark.favicon')
    description = serializers.URLField(source='bookmark.description')

    class Meta:
        model = Favorite
        fields = ['url', 'title', 'favicon', 'description']