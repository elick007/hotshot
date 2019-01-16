from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from hotshot.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, DailyVideo, HotVideo, HotShotUser, UserFavorite, \
    DYHotVideoModel


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')


class UserFavoriteSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = UserFavorite
        fields = ('id', 'description', 'cover', 'playUrl')


class UserSerializer(serializers.ModelSerializer):
    # snippet = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('username', 'password',)


class DailyVideoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField

    class Meta:
        model = DailyVideo
        fields = ('id', 'created', 'title', 'description', 'cover', 'playUrl')


class HotVideoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField

    class Meta:
        model = HotVideo
        fields = ('id', 'created', 'title', 'description', 'cover', 'playUrl')


class DYHotVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DYHotVideoModel
        fields = ('id', 'created', 'author', 'view', 'description', 'cover', 'playUrl')


class LSPHotVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotVideo
        fields = ('id', 'created', 'title', 'description', 'cover', 'playUrl')
