import uuid

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from hotshot.models import OpenEyesDailyVideo, OpenEyesHotVideo, HotShotUser, \
    UserFavoriteOEModel, \
    DYHotVideoModel, SMSModel, UserFavoriteDYModel, UserFavoriteLSPModel, LSPHotVideoModel, PublicVideoModel, \
    OECommentModel


class HotShotUserSerializer(serializers.ModelSerializer):
    # snippet = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    class Meta:
        model = HotShotUser
        fields = ('username', 'avatar', 'uid', 'phone')


class HotShotUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotShotUser
        fields = ('username', 'phone', 'password', 'uid')


class UploadAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    suffix = serializers.CharField(allow_blank=False)

    class Meta:
        model = HotShotUser
        fields = ('avatar', 'suffix')


class UploadPublicVideoSerializer(serializers.ModelSerializer):
    video = serializers.FileField(allow_empty_file=False, use_url=True)
    content = serializers.CharField(default='', allow_blank=True, max_length=200)
    suffix = serializers.CharField(allow_blank=False, max_length=100)

    class Meta:
        model = PublicVideoModel
        fields = ('video', 'content', 'suffix')


class PublicVideoSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        if obj.author:
            return {'userName': obj.author.username, 'avatar': '/media/' + str(obj.author.avatar)}
        return None

    class Meta:
        model = PublicVideoModel
        fields = ('content', 'cover', 'playUrl', 'author','created')
        depth = 1


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotShotUser
        fields = ('username', 'avatar')


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
        fields = ('id', 'created', 'type', 'date', 'duration', 'title', 'description', 'cover', 'playUrl')


class DYHotVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DYHotVideoModel
        fields = (
            'id', 'created', 'type', 'date', 'duration', 'author', 'view', 'description', 'cover', 'playUrl', 'author')


class LSPHotVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LSPHotVideoModel
        # fields = ('id', 'created', 'type', 'date', 'duration', 'title', 'description', 'cover', 'playUrl')
        fields = '__all__'


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
        fields = '__all__'


class UserFavoriteOEListSerializer(serializers.ModelSerializer):
    video = OpenEyesHotVideoSerializer()

    class Meta:
        model = OpenEyesHotVideo
        fields = ('video', 'id')


class UserFavoriteDYSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteDYModel
        validators = [
            UniqueTogetherValidator(
                queryset=UserFavoriteDYModel.objects.all(),
                fields=('uid', 'video'),
                message='已经收藏'
            )
        ]
        fields = ('id', 'uid', 'video')


class UserFavoriteDYListSerializer(serializers.ModelSerializer):
    video = DYHotVideoSerializer()

    class Meta:
        model = DYHotVideoModel
        fields = ('id', 'video')


class UserFavoriteLSPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteLSPModel
        validators = [
            UniqueTogetherValidator(
                queryset=UserFavoriteLSPModel.objects.all(),
                fields=('uid', 'video'),
                message='已经收藏'
            )
        ]
        fields = ('id', 'uid', 'video')


class UserFavoriteLSPListSerializer(serializers.ModelSerializer):
    video = LSPHotVideoSerializer

    class Meta:
        model = LSPHotVideoModel
        fields = ('id', 'video')


class OECommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OECommentModel
        fields = ('__all__')


class OECommentListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        if obj.user:
            return {'userName': obj.user.username, 'avatar': '/media/' + str(obj.user.avatar)}

    class Meta:
        model=OECommentModel
        fields = ('user', 'content')
        depth = 1
