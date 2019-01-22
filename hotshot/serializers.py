import uuid

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from hotshot.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, OpenEyesDailyVideo, OpenEyesHotVideo, HotShotUser, \
    UserFavoriteOEModel, \
    DYHotVideoModel, SMSModel


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')


class UserFavoriteOESerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteOEModel
        validators = [
            UniqueTogetherValidator(
                queryset=UserFavoriteOEModel.objects.all(),
                fields=('uid', 'video'),
                message='已经收藏'
            )
        ]
        fields = ('id', 'uid', 'video')


class UserSerializer(serializers.ModelSerializer):
    # snippet = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = HotShotUser
        fields = ('username', 'password', 'uid')


class SMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSModel
        fields = ('phone', 'code', 'timestamp')


class OpenEyesDailyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenEyesDailyVideo
        fields = ('id', 'created', 'title', 'description', 'cover', 'playUrl')


class OpenEyesHotVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenEyesHotVideo
        fields = ('id', 'created', 'title', 'description', 'cover', 'playUrl')


class DYHotVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DYHotVideoModel
        fields = ('id', 'created', 'author', 'view', 'description', 'cover', 'playUrl')


class LSPHotVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenEyesHotVideo
        fields = ('id', 'created', 'title', 'description', 'cover', 'playUrl')
