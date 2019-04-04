from django.conf.urls import url
from django.urls import path, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from MyProject import settings
from hotshot import views
from rest_framework.authtoken import views as rest_views
from hotshot.views import DailyVideoViewSet, OEHotVideoViewSet, \
    DYHotVideoViewSet, LSPHotVideoViewSet, UserFavoriteOEView, OERandomVideoViewSet


daily_video_list = DailyVideoViewSet.as_view({
    'get': 'list'
})
hot_video_list = OEHotVideoViewSet.as_view({
    'get': 'list'
})
DY_hot_video_list = DYHotVideoViewSet.as_view({
    'get': 'list'
})
LSP_hot_video_list = LSPHotVideoViewSet.as_view({
    'get': 'list'
})
# user_favorite_OE = UserFavoriteOEView.as_view({
#     'get': 'list'
# })
oe_random_video = OERandomVideoViewSet.as_view({
    'get': 'list'
})
dy_random_video = views.DYRandomVideoViewSet.as_view({
    'get': 'list'
})
lsp_random_video = views.LSPRandomVideoViewSet.as_view({
    'get': 'list'
})
router = DefaultRouter()
# router.register(r'api/user', views.UserViewSet)
router.register(r'api/videos/oe/daily', views.DailyVideoViewSet)
router.register(r'api/videos/oe/hot', views.OEHotVideoViewSet)
# router.register(r'api/videos/oe/random', OERandomVideoViewSet)
router.register(r'api/videos/dy/hot', views.DYHotVideoViewSet)
# router.register(r'api/videos/dy/random', views.DYRandomVideoViewSet)
router.register(r'api/videos/lsp/hot', views.LSPHotVideoViewSet)
router.register(r'api/videos/public/info',views.PublicVideoView)
# router.register(r'api/videos/lsp/random', views.LSPRandomVideoViewSet)
# router.register(r'api/user/favorite/oe', views.UserFavoriteOEView)
# router.register(r'api/user/favorite/dy', views.UserFavoriteDYView)
# router.register(r'api/user/favorite/lsp', views.UserFavoriteLSPView)
# urlpatterns_hotshot = [
#     path('', include(router.urls)),
# ]
urlpatterns_hotshot = [
    path('', include(router.urls)),
    url(r'^api-token-auth/', rest_views.obtain_auth_token),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('api/user/login/',views.UserLoginViews.as_view(),name='login'),
    path('api/user/register/', views.UserRegisterView.as_view(), name='register'),
    path('api/user/verify/', views.SMSView.as_view(), name='verify'),
    path('api/user/avatar/', views.AvatarUploadView.as_view(), name='avatar'),
    path('api/videos/oe/random/', oe_random_video, name='api/videos/oe/random'),
    path('api/videos/dy/random/', dy_random_video, name='api/videos/dy/random'),
    path('api/videos/lsp/random/', lsp_random_video, name='api/videos/lsp/random'),
    path('api/videos/public/upload/',views.PublicVideoUploadView.as_view(),name='pub_video_upload'),
    path('api/user/favorite/oe/', views.UserFavoriteOEView.as_view(), name='api/user/favorite/oe'),
    path('api/user/favorite/dy/', views.UserFavoriteDYView.as_view(), name='api/user/favorite/dy'),
    path('api/user/favorite/lsp/', views.UserFavoriteLSPView.as_view(), name='api/user/favorite/lsp'),
]
