from rest_framework import serializers

from main.models import Bookmark

#Сериалайзер POST запроса, по ТЗ требуется, чтобы пользователь только URL достаточно было ввести
class MainPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['url']

class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'favicon']


class MainDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'title', 'description', 'url', 'time_created']