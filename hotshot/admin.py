from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from hotshot.models import HotShotUser


class ProfileInline(admin.StackedInline):
    model = HotShotUser
    can_delete = False
    verbose_name_plural = "profile"

class UserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.register(User, UserAdmin)