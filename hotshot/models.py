from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from rest_framework.authtoken.models import Token

from MyProject import settings

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class HotShotUser(AbstractUser):
    # username = models.OneToOneField(User, on_delete=models.CASCADE)
    # password = models.OneToOneField(User,on_delete=models.CASCADE)
    # username = models.CharField(max_length=8, default='', unique=True)
    # password = models.CharField(max_length=13)
    # created = models.DateTimeField(auto_now_add=True)
    uid = models.CharField(unique=True, default='', max_length=13)
    phone = models.CharField(unique=True, blank=False, null=False, max_length=11)
    avatar = models.ImageField(upload_to="avatar/%Y/%m/%d", blank=False, default="avatar/default.jpg")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


class SMSModel(models.Model):
    phone = models.CharField(max_length=11, default='', unique=True)
    code = models.CharField(max_length=6, default='')
    timestamp = models.CharField(max_length=10, default='')

    class Meta:
        pass


class OpenEyesDailyVideo(models.Model):
    created = models.DateTimeField(auto_now=True)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    cover = models.TextField(default='')
    playUrl = models.TextField(default='')

    class Meta:
        ordering = ('created',)


class OpenEyesHotVideo(models.Model):
    created = models.DateTimeField(auto_now=True)
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, default='')  # 视频类型 开眼目前有两种 hot和daily
    date = models.CharField(max_length=100, default='')  # 时间戳
    duration = models.CharField(max_length=100, default='')  # 视频长度
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    cover = models.TextField(default='')
    playUrl = models.TextField(default='')

    class Meta:
        ordering = ('created',)


class DYHotVideoModel(models.Model):
    created = models.DateTimeField(auto_now=True)
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, default='')  # 视频类型 抖音目前有两种 hot和positive
    date = models.CharField(max_length=100, default='')  # 时间戳
    duration = models.CharField(max_length=100, default='')  # 视频长度
    author = models.CharField(max_length=100, default='')
    view = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True, default='')
    cover = models.TextField(default='')
    playUrl = models.TextField(default='')

    class Meta:
        ordering = ('created',)


class LSPHotVideoModel(models.Model):
    created = models.DateTimeField(auto_now=True)
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, default='')  # 视频类型 梨视频类型过多统一为hot
    date = models.CharField(max_length=100, default='')  # 时间戳
    duration = models.CharField(max_length=100, default='')  # 视频长度
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    cover = models.TextField(default='')
    playUrl = models.TextField(default='')
    author = models.CharField(max_length=100, default='')

    class Meta:
        ordering = ('created',)


class UserFavoriteOEModel(models.Model):
    uid = models.ForeignKey(HotShotUser, related_name='oe_fav_uid', on_delete=models.CASCADE)
    video = models.ForeignKey(OpenEyesHotVideo, related_name='oe_fav_video', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('uid', 'video')
        ordering = ('-created',)


class UserFavoriteDYModel(models.Model):
    uid = models.ForeignKey(HotShotUser, related_name='dy_favorite_uid', on_delete=models.CASCADE)
    video = models.ForeignKey(DYHotVideoModel, related_name='dy_favorite_video', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('uid', 'video')
        ordering = ('-created',)


class UserFavoriteLSPModel(models.Model):
    uid = models.ForeignKey(HotShotUser, related_name='lsp_favorite_uid', on_delete=models.CASCADE)
    video = models.ForeignKey(LSPHotVideoModel, related_name='lsp_favorite_video', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('uid', 'video')
        ordering = ('-created',)


# class AuthorModel(models.Model):
#     username = models.OneToOneField(HotShotUser.username, related_name='author_name', on_delete=models.CASCADE)
#     avatar = models.OneToOneField(HotShotUser.avatar, related_name='author_avatar', on_delete=models.CASCADE)


class PublicVideoModel(models.Model):
    content = models.TextField(default='')
    playUrl = models.FileField(upload_to='public/video/%Y/%m/%d', blank=False, max_length=50 * 1024 * 1024)
    cover = models.ImageField(upload_to='public/cover/%Y/%m/%d', blank=False,max_length=1024*1024)
    author = models.ForeignKey(HotShotUser, related_name='public_video_author', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
