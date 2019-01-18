from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from hotshot import views
from hotshot.views import SnippetViewSet, UserViewSet, DailyVideoViewSet, HotVideoViewSet,  \
    DYHotVideoViewSet, LSPHotVideoViewSet

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
# urlpatterns = [
#     path('snippets/', snippet_list, name='snippet_list'),
#     path('snippets/<int:pk>/', snippet_detail, name='snippet_detail'),
#     # path('api/user/', user, name='user'),
#     path('api/user/', views.UserViews.as_view()),
#     path('api/videos/daily/', daily_video_list, name='daily_video_list'),
#     path('api/videos/hot/', hot_video_list, name='hot_video_list'),
#     path('api/videos/douyin/hot/video/', DY_hot_video_list, name='DY_hot_video_list'),
#     path('api/videos/lsp/hot/video/', LSP_hot_video_list, name='lsp_hot_video_list'),
#     path('api/user/register/', UserRegister, name='user_register'),
#     # path('api/user/favorite/', user_favorite, name='user_favorite')
#     path('api/user/favorite/', views.UserFavoriteView.as_view())
# ]
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
# router.register(r'api/user', views.UserViewSet)
router.register(r'api/videos/daily', views.DailyVideoViewSet)
router.register(r'api/videos/hot', views.HotVideoViewSet)
router.register(r'api/videos/douyin/hot', views.DYHotVideoViewSet)
router.register(r'api/videos/lsp/hot', views.LSPHotVideoViewSet)
# urlpatterns_hotshot = [
#     path('', include(router.urls)),
# ]
urlpatterns_hotshot = [
    path('', include(router.urls)),
    path('api/videos/daily/', daily_video_list, name='daily_video_list'),
    path('api/user/', views.UserViews.as_view(), name='user'),
]
