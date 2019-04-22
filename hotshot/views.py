import os
import time
import uuid

import cv2
from PIL import Image
from django.contrib.auth.models import User
from rest_framework import status, authentication, permissions, parsers, renderers
from rest_framework import viewsets
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.views import APIView

from MyProject import settings
from hotshot import serializers, models
from hotshot.base.custom_pagination import LargeResultsSetPagination
from hotshot.base.restbase import CustomViewBase, CustomResponse, CustomReadOnlyViewSet
from hotshot.models import OpenEyesDailyVideo, OpenEyesHotVideo, DYHotVideoModel, \
    LSPHotVideoModel, HotShotUser, SMSModel, UserFavoriteOEModel, UserFavoriteDYModel, UserFavoriteLSPModel, \
    PublicVideoModel
from hotshot.permissions import IsOwnerOrReadOnly
from hotshot.serializers import HotShotUserSerializer, OpenEyesDailyVideoSerializer, \
    OpenEyesHotVideoSerializer, \
    UserFavoriteOESerializer, DYHotVideoSerializer, LSPHotVideoSerializer, SMSSerializer, UserFavoriteOEListSerializer, \
    UserFavoriteDYSerializer, UserFavoriteDYListSerializer, UserFavoriteLSPSerializer, UserFavoriteLSPListSerializer, \
    UploadAvatarSerializer, UploadPublicVideoSerializer, PublicVideoSerializer, OECommentSerializer
from rest_framework import generics
from hotshot.utils.userutil import verify_phone
from hotshot.utils.yunxin import Yunxin


# @api_view(['GET', 'POST'])
# def snippet_list(request):
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class UserLoginViews(APIView):
    queryset = HotShotUser.objects.all()
    serializer_class = HotShotUserSerializer

    def post(self, request, format=None):
        username_post = request.data.get('username', '')
        password_post = request.data.get('password', '')
        if username_post != '':
            user = None
            if HotShotUser.objects.filter(username__exact=username_post):
                user = HotShotUser.objects.get(username__exact=username_post)
            elif HotShotUser.objects.filter(phone__exact=username_post):
                user = HotShotUser.objects.get(phone__exact=username_post)
                # return CustomResponse(code=100, msg='用户不存在', data=None, status=status.HTTP_204_NO_CONTENT)
            if user:
                if user.check_password(password_post):
                    serializer = serializers.HotShotUserSerializer(user)
                    return CustomResponse(code=1, msg='login success', data=serializer.data, status=status.HTTP_200_OK)
                return CustomResponse(code=101, msg='密码错误', status=status.HTTP_400_BAD_REQUEST)
            return CustomResponse(code=100, msg='用户不存在', data=None, status=status.HTTP_204_NO_CONTENT)
        return CustomResponse(code=100, msg='用户不存在', data=None, status=status.HTTP_204_NO_CONTENT)
        # if phone != '':
        #     if not HotShotUser.objects.filter(phone__exact=phone):
        #         return CustomResponse(code=102, msg='手机号不存在', data=None, status=status.HTTP_400_BAD_REQUEST)
        #     user = HotShotUser.objects.get(phone__exact=phone)
        #     if user.check_password(password_post):
        #         serializer = serializers.HotShotUserSerializer(user)
        #         return CustomResponse(code=1, msg='login success', data=serializer.data, status=status.HTTP_200_OK)
        #     return CustomResponse(code=101, msg='密码错误', status=status.HTTP_400_BAD_REQUEST)
        # serializer = serializers.HotShotUserSerializer(data=request.data)
        # return CustomResponse(code=201, msg=serializer.errors, data=None, status=status.HTTP_400_BAD_REQUEST)
        # if ac == 'change':
        #     if verify_code == '' or phone == '':
        #         return CustomResponse(code=0, msg='verifyCode or phone empty', status=status.HTTP_400_BAD_REQUEST)
        #     if not HotShotUser.objects.filter(phone=phone).exists():
        #         return CustomResponse(code=0, msg='phone don\'t exist', data='', status=status.HTTP_400_BAD_REQUEST)
        #     smsModel = SMSModel.objects.filter(phone=phone, code=verify_code)
        #     if smsModel.exists():
        #         dt_now = int(time.time())
        #         dt_old = int(smsModel[0].timestamp)
        #         if (dt_now - dt_old) <= 10 * 60:  # 验证码10分钟有效
        #             user_model = HotShotUser.objects.filter(phone=phone).update(password=password_post)
        #             if user_model == 1:
        #                 return CustomResponse(code=1, msg='change password success', data='', status=status.HTTP_200_OK)
        #             return CustomResponse(code=0, msg='change password fail', data='',
        #                                   status=status.HTTP_503_SERVICE_UNAVAILABLE)
        #         return CustomResponse(code=0, msg='verifyCode error', status=status.HTTP_400_BAD_REQUEST)
        #     return CustomResponse(code=0, msg='verifyCode error', status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):
    queryset = HotShotUser.objects.all()
    serializer_class = HotShotUserSerializer

    def post(self, request, format=None):
        verify = request.data.get('verify', '')
        username = request.data.get('username', '')
        phone = request.data.get('phone', '')
        if verify == '':
            return CustomResponse(data=None, code=103, msg="verify is empty", status=status.HTTP_400_BAD_REQUEST)
        if HotShotUser.objects.filter(phone__exact=phone):
            return CustomResponse(code=104, msg='phone exist', data='', status=status.HTTP_400_BAD_REQUEST)
        if HotShotUser.objects.filter(username__exact=username):
            return CustomResponse(code=105, msg='username exist', data='', status=status.HTTP_400_BAD_REQUEST)
        serializers = HotShotUserSerializer(data=request.data)
        smsModel = SMSModel.objects.filter(phone=phone, code=verify)
        if smsModel.exists():
            dt_now = int(time.time())
            dt_old = int(smsModel[0].timestamp)
            if (dt_now - dt_old) <= 10 * 60:  # 验证码10分钟有效
                if serializers.is_valid():
                    user = serializers.save()
                    # 加密密码
                    user.set_password(request.data['password'])
                    uid = uuid.uuid1().int >> 108
                    HotShotUser.objects.filter(id=user.id).update(password=user.password, is_active=True, uid=uid)
                    return CustomResponse(data=serializers.data, code=1, msg="success", status=status.HTTP_200_OK)
                return CustomResponse(data=serializers.errors, code=201, msg='fail', status=status.HTTP_400_BAD_REQUEST)
            return CustomResponse(data=None, code=106, msg='verify invalid', status=status.HTTP_400_BAD_REQUEST)
        return CustomResponse(data=None, code=201, msg="param error", status=status.HTTP_400_BAD_REQUEST)


class SMSView(APIView):
    def get(self, request, format=None):
        phone = self.request.GET.get('phone')
        if verify_phone(phone=phone):
            yunxin = Yunxin()
            sms_response = yunxin.get_sms(phone=phone)
            if sms_response is not None and sms_response['code'] == 200:
                sms_code = sms_response['obj']
                SMSModel.objects.update_or_create(phone=phone,
                                                  defaults={'code': sms_code, 'timestamp': str(int(time.time()))})
                return CustomResponse(code=1, msg="require msm code success", data='', status=status.HTTP_200_OK)
            return CustomResponse(code=107, msg='can not get msm code from yunxin',
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return CustomResponse(code=108, msg='phone error', data='', status=status.HTTP_400_BAD_REQUEST)


class AvatarUploadView(APIView):
    throttle_classes = ()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,
                      parsers.JSONParser, parsers.FileUploadParser,)

    def post(self, request, format='json'):
        serializers = UploadAvatarSerializer(data=request.data)
        if serializers.is_valid():
            suffix = request.data.get('suffix').split('.')[1]
            user = HotShotUser.objects.get(username__exact=request.user.username)
            avatar_name = user.uid + "." + suffix
            avatar = Image.open(request.data['avatar'])
            avatar_file_path = os.path.join(settings.MEDIA_ROOT, 'avatar/' + avatar_name)
            avatar.save(avatar_file_path)
            HotShotUser.objects.filter(id=request.user.id).update(avatar='avatar/' + avatar_name)
            return CustomResponse(data=None, code=1, msg='success', status=status.HTTP_200_OK)
        return CustomResponse(data=serializers.errors, code=0, msg='fail', status=status.HTTP_400_BAD_REQUEST)


class PublicVideoUploadView(APIView):
    throttle_classes = ()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,
                      parsers.JSONParser, parsers.FileUploadParser,)

    def post(self, request, format='json'):
        serializers = UploadPublicVideoSerializer(data=request.data)
        if serializers.is_valid():
            suffix = request.data.get('suffix').split('.')[1]
            video = request.data['video']
            random = str(uuid.uuid1().time)
            video_name = random + '.' + suffix
            video_path = os.path.join(settings.MEDIA_ROOT + '/public/video/', video_name)
            video_stream = open(video_path, 'wb+')
            for chunk in video.chunks():
                video_stream.write(chunk)
            video_stream.close()
            # 获取第一帧
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_MSEC, 1)
            success, image = cap.read()
            if success:
                image_path = os.path.join(settings.MEDIA_ROOT + '/public/cover/', random + '.jpg')
                cv2.imwrite(image_path, image)
                author = HotShotUser.objects.get(id=request.user.id)
                public_video = PublicVideoModel()
                public_video.playUrl = 'public/video/' + video_name
                public_video.content = request.data.get('content', '')
                public_video.cover = 'public/cover/' + random + '.jpg'
                public_video.author = author
                public_video.save()
            return CustomResponse(data=None, code=1, msg='success', status=status.HTTP_200_OK)
        return CustomResponse(data=None, code=0, msg=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicVideoView(CustomReadOnlyViewSet):
    queryset = PublicVideoModel.objects.order_by('-created')
    serializer_class = PublicVideoSerializer


# class SnippetViewSet(viewsets.ModelViewSet):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
#
#     @action(detail=True)
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

class DailyVideoViewSet(CustomReadOnlyViewSet):
    queryset = OpenEyesDailyVideo.objects.order_by('-created')
    serializer_class = OpenEyesDailyVideoSerializer


class OEHotVideoViewSet(CustomReadOnlyViewSet):
    queryset = OpenEyesHotVideo.objects.order_by('-created')
    serializer_class = OpenEyesHotVideoSerializer
    pagination_class = LargeResultsSetPagination


class OERandomVideoViewSet(CustomReadOnlyViewSet):
    queryset = OpenEyesHotVideo.objects.order_by('?')[:10]
    serializer_class = OpenEyesHotVideoSerializer


class DYHotVideoViewSet(CustomReadOnlyViewSet):
    queryset = DYHotVideoModel.objects.order_by('-created')[:30]
    serializer_class = DYHotVideoSerializer
    pagination_class = LargeResultsSetPagination


class DYRandomVideoViewSet(CustomReadOnlyViewSet):
    queryset = DYHotVideoModel.objects.order_by('?')[:10]
    serializer_class = DYHotVideoSerializer


class LSPHotVideoViewSet(CustomReadOnlyViewSet):
    queryset = LSPHotVideoModel.objects.order_by('-created')[:30]
    serializer_class = LSPHotVideoSerializer
    pagination_class = LargeResultsSetPagination


class LSPRandomVideoViewSet(CustomReadOnlyViewSet):
    queryset = LSPHotVideoModel.objects.order_by('?')[:10]
    serializer_class = LSPHotVideoSerializer


class UserFavoriteOEView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        ac = self.request.GET.get('ac')
        if ac == 'list':
            model = UserFavoriteOEModel.objects.filter(uid=request.user.id)
            serializer = UserFavoriteOEListSerializer(model, many=True)
            return CustomResponse(data=serializer.data, code=1, msg='success', status=status.HTTP_200_OK)
        elif ac == "retrieve":
            video_id = self.request.GET.get('video_id')
            model = UserFavoriteOEModel.objects.filter(uid=request.user.id, video_id=video_id)
            if model.exists():
                serializer = UserFavoriteOEListSerializer(model, many=True)
                return CustomResponse(data=serializer.data, code=1, msg='exist', status=status.HTTP_200_OK)
            else:
                return CustomResponse(data=None, code=0, msg='don\'t exist', status=status.HTTP_404_NOT_FOUND)
        return CustomResponse(data=None, code=0, msg='parameter error', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        ac = self.request.GET.get('ac')
        if ac == 'add':
            data = {'uid': request.user.id, 'video': request.data['video_id']}
            serializer = UserFavoriteOESerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(data=serializer.data, code=1, msg='success', status=status.HTTP_200_OK)
            return CustomResponse(data=serializer.errors, code=0, msg='fail', status=status.HTTP_400_BAD_REQUEST)
        elif ac == 'del':
            model = UserFavoriteOEModel.objects.filter(uid=request.user.id,
                                                       video_id=self.request.data.get('video_id'))
            if model.exists():
                model.delete()
                return CustomResponse(data=None, code=1, msg='success', status=status.HTTP_200_OK)
            return CustomResponse(data=None, code=0, msg='未收藏相关视频', status=status.HTTP_204_NO_CONTENT)


class UserFavoriteDYView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        ac = self.request.GET.get('ac')
        if ac == 'list':
            model = UserFavoriteDYModel.objects.filter(uid=request.user.id)
            serializer = UserFavoriteDYListSerializer(model, many=True)
            return CustomResponse(data=serializer.data, code=1, msg='success', status=status.HTTP_200_OK)
        elif ac == "retrieve":
            video_id = self.request.GET.get('video_id')
            model = UserFavoriteDYModel.objects.filter(uid=request.user.id, video_id=video_id)
            if model.exists():
                serializer = UserFavoriteDYListSerializer(model, many=True)
                return CustomResponse(data=serializer.data, code=1, msg='exist', status=status.HTTP_200_OK)
            else:
                return CustomResponse(data=None, code=0, msg='don\'t exist', status=status.HTTP_404_NOT_FOUND)
        return CustomResponse(data=None, code=0, msg='parameter error', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        ac = self.request.GET.get('ac')
        if ac == 'add':
            data = {'uid': request.user.id, 'video': request.data['video_id']}
            serializer = UserFavoriteDYSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(data=serializer.data, code=1, msg='success', status=status.HTTP_200_OK)
            return CustomResponse(data=serializer.errors, code=0, msg='fail', status=status.HTTP_400_BAD_REQUEST)
        elif ac == 'del':
            model = UserFavoriteDYModel.objects.filter(uid=request.user.id,
                                                       video_id=self.request.data.get('video_id'))
            if model.exists():
                model.delete()
                return CustomResponse(data=None, code=1, msg='success', status=status.HTTP_200_OK)
            return CustomResponse(data=None, code=0, msg='未收藏相关视频', status=status.HTTP_204_NO_CONTENT)


class UserFavoriteLSPView(APIView):
    def get(self, request, format=None):
        ac = self.request.GET.get('ac')
        if ac == 'list':
            model = UserFavoriteLSPModel.objects.filter(uid=request.user.id)
            serializer = UserFavoriteLSPListSerializer(model, many=True)
            return CustomResponse(data=serializer.data, code=1, msg='success', status=status.HTTP_200_OK)
        elif ac == "retrieve":
            video_id = self.request.GET.get('video_id')
            model = UserFavoriteLSPModel.objects.filter(uid=request.user.id, video_id=video_id)
            if model.exists():
                serializer = UserFavoriteLSPListSerializer(model, many=True)
                return CustomResponse(data=serializer.data, code=1, msg='exist', status=status.HTTP_200_OK)
            else:
                return CustomResponse(data=None, code=0, msg='don\'t exist', status=status.HTTP_404_NOT_FOUND)
        return CustomResponse(data=None, code=0, msg='parameter error', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        ac = self.request.GET.get('ac')
        if ac == 'add':
            data = {'uid': request.user.id, 'video': request.data['video_id']}
            serializer = UserFavoriteLSPSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(data=serializer.data, code=1, msg='success', status=status.HTTP_200_OK)
            return CustomResponse(data=serializer.errors, code=0, msg='fail', status=status.HTTP_400_BAD_REQUEST)
        elif ac == 'del':
            model = UserFavoriteLSPModel.objects.filter(uid=request.user.id,
                                                        video_id=self.request.data.get('video_id'))
            if model.exists():
                model.delete()
                return CustomResponse(data=None, code=1, msg='success', status=status.HTTP_200_OK)
            return CustomResponse(data=None, code=0, msg='未收藏相关视频', status=status.HTTP_204_NO_CONTENT)


class OECommentView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        data = {'user': request.user.id, 'video': request.data.get('videoId'), 'content': request.data.get('content')}
        serializer = OECommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(data='', code=1, msg='success', status=status.HTTP_200_OK)
        return CustomResponse(data=None, code=0, msg=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OECommentListView(APIView):
    def get(self, request, format=None):
        object = models.OECommentModel.objects.filter(video_id=request.GET.get('videoId'))
        serializer = serializers.OECommentListSerializer(object, many=True)
        return CustomResponse(data=serializer.data, code=1, msg='success', status=status.HTTP_200_OK)
