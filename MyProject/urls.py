"""MyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hotshot import views

# router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet)
# #router.register(r'api/user', views.UserViewSet)
# router.register(r'daily video', views.DailyVideoViewSet)
# router.register(r'hot video', views.HotVideoViewSet)
# router.register(r'douyin hot video', views.DYHotVideoViewSet)
# router.register(r'lsp hot video', views.LSPHotVideoViewSet)
# router.register(r'api/user/favorite', views.UserFavoriteViewSet)
# router.register(r'api/user/register', views.UserRegister)
from hotshot.urls import router, urlpatterns_hotshot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urlpatterns_hotshot)),
]
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
