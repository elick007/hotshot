from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from hotshot import views
from hotshot.views import SnippetViewSet, UserViewSet, DailyVideoViewSet, HotVideoViewSet, \
    DYHotVideoViewSet, LSPHotVideoViewSet, UserFavoriteOEView

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
user = UserViewSet.as_view({
    'post': 'create'
})

daily_video_list = DailyVideoViewSet.as_view({
    'get': 'list'
})
hot_video_list = HotVideoViewSet.as_view({
    'get': 'list'
})
DY_hot_video_list = DYHotVideoViewSet.as_view({
    'get': 'list'
})
LSP_hot_video_list = LSPHotVideoViewSet.as_view({
    'get': 'list'
})
user_favorite_OE = UserFavoriteOEView.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
# router.register(r'api/user', views.UserViewSet)
router.register(r'api/videos/oe/daily', views.DailyVideoViewSet)
router.register(r'api/videos/oe/hot', views.HotVideoViewSet)
router.register(r'api/videos/dy/hot', views.DYHotVideoViewSet)
router.register(r'api/videos/lsp/hot', views.LSPHotVideoViewSet)
router.register(r'api/user/favorite/oe',views.UserFavoriteOEView)
router.register(r'api/user/favorite/dy',views.UserFavoriteDYView)
router.register(r'api/user/favorite/lsp',views.UserFavoriteLSPView)
# urlpatterns_hotshot = [
#     path('', include(router.urls)),
# ]
urlpatterns_hotshot = [
    path('', include(router.urls)),
    path('api/user/', views.UserViews.as_view(), name='user'),
    path('api/user/verify/', views.SMSView.as_view(), name='verify')
]
