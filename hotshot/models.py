from django.contrib.auth.models import AbstractUser, User
from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)


class HotShotUser(models.Model):
    # username = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=8, default='', unique=True)
    password = models.CharField(max_length=13)
    created = models.DateTimeField(auto_now_add=True)
    uid = models.CharField(primary_key=True, unique=True, default='', max_length=13)
    phone = models.CharField(unique=True, default='', max_length=11)

    class Meta:
        pass


class SMSModel(models.Model):
    phone = models.CharField(max_length=11, default='', unique=True)
    code = models.CharField(max_length=6, default='')
    timestamp = models.CharField(max_length=10, default='')

    class Meta:
        pass


#
# class UserFavorite(models.Model):
#     owner = models.ForeignKey('auth.User', related_name='favorite', on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     description = models.TextField(blank=True, default='')
#     cover = models.TextField(default='')
#     playUrl = models.TextField(default='')
#
#     class Meta:
#         ordering = ('created',)


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
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    cover = models.TextField(default='')
    playUrl = models.TextField(default='')

    class Meta:
        ordering = ('created',)


class DYHotVideoModel(models.Model):
    created = models.DateTimeField(auto_now=True)
    id = models.AutoField(primary_key=True)
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
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    cover = models.TextField(default='')
    playUrl = models.TextField(default='')

    class Meta:
        ordering = ('created',)


class UserFavoriteOEModel(models.Model):
    uid = models.ForeignKey(HotShotUser, related_name='oe_favorite_uid', on_delete=models.CASCADE)
    video = models.ForeignKey(OpenEyesHotVideo, related_name='oe_favorite_video', on_delete=models.CASCADE)
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
