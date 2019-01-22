import time
import uuid
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins
from hotshot.base.restbase import CustomViewBase, CustomResponse, CustomReadOnlyViewSet
from hotshot.models import Snippet, OpenEyesDailyVideo, OpenEyesHotVideo, DYHotVideoModel, \
    LSPHotVideoModel, HotShotUser, SMSModel, UserFavoriteOEModel
from hotshot.permissions import IsOwnerOrReadOnly
from hotshot.serializers import SnippetSerializer, UserSerializer, OpenEyesDailyVideoSerializer, \
    OpenEyesHotVideoSerializer, \
    UserFavoriteOESerializer, DYHotVideoSerializer, LSPHotVideoSerializer, SMSSerializer
from rest_framework import generics

from hotshot.utils.aesutil import decrypt_oralce
from hotshot.utils.userutil import verify_phone
from hotshot.utils.yunxin import Yunxin


@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_ac(request):
    if request.method == 'POST':
        uid = uuid.uuid1().int >> 90
        serializer = UserSerializer(data=request.data, uid=uid)
        if serializer.is_valid():
            return Response(data='diaomao', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViews(APIView):

    def post(self, request, format=None):
        ac = self.request.GET.get('ac')
        username_post = request.data['username']
        password_post = decrypt_oralce(request.data['password'])
        if ac == 'login':
            login_dict = HotShotUser.objects.filter(username=username_post, password=password_post)
            if login_dict.exists():
                data = {'uid': '%s' % login_dict[0].uid}
                return CustomResponse(code=1, msg='login success', data=data, status=status.HTTP_200_OK)
            return CustomResponse(code=0, msg='username or password error', status=status.HTTP_200_OK)
        if ac == 'register':
            verify_code = request.data.get('verifyCode', '')
            phone = request.data.get('phone', '')
            if verify_code == '' or phone == '':
                return CustomResponse(code=0, msg='verifyCode or phone empty')
            if HotShotUser.objects.filter(phone=phone).exists():
                return CustomResponse(code=0, msg='phone exist', data='', status=status.HTTP_400_BAD_REQUEST)
            if HotShotUser.objects.filter(username=username_post):
                return CustomResponse(code=0, msg='username exist', data='', status=status.HTTP_400_BAD_REQUEST)
            smsModel = SMSModel.objects.filter(phone=phone, code=verify_code)
            if smsModel.exists():
                dt_now = int(time.time())
                dt_old = int(smsModel[0].timestamp)
                print((dt_now - dt_old))
                if (dt_now - dt_old) <= 10 * 60:  # 验证码10分钟有效
                    uid = uuid.uuid1().int >> 90
                    # userModel = HotShotUser.objects.create(username=username_post, password=password_post, uid=str(uid),
                    #                                      phone=phone)
                    save_data = {'username': username_post, 'password': password_post, 'phone': phone, 'uid': str(uid)}
                    serializer = UserSerializer(data=save_data)
                    if serializer.is_valid():
                        serializer.save()
                        return CustomResponse(code=1, msg='register success', data='', status=status.HTTP_200_OK)
                    return CustomResponse(code=0, msg='insert user fail', data='',
                                          status=status.HTTP_503_SERVICE_UNAVAILABLE)
            return CustomResponse(code=0, msg='verifyCode error', status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        return CustomResponse(status=status.HTTP_400_BAD_REQUEST)


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
            return CustomResponse(code=0, msg='can not get msm code from yunxin',
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return CustomResponse(code=0, msg='phone error', data='', status=status.HTTP_400_BAD_REQUEST)


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @action(detail=True)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserFavoriteOEView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = UserFavoriteOESerializer
    queryset = UserFavoriteOEModel.objects.all()

    def get_queryset(self):
        return UserFavoriteOEModel.objects.filter(uid=self.request.data.get('uid'))


class UserViewSet(viewsets.ModelViewSet):
    queryset = HotShotUser.objects.all()
    serializer_class = UserSerializer

    # def list(self, request, *args, **kwargs):
    #     return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        uid = uuid.uuid1().int >> 90
        if serializer.is_valid():
            serializer.save(uid=str(uid))


class DailyVideoViewSet(CustomReadOnlyViewSet):
    queryset = OpenEyesDailyVideo.objects.all().order_by('-created')
    serializer_class = OpenEyesDailyVideoSerializer


class HotVideoViewSet(CustomReadOnlyViewSet):
    queryset = OpenEyesHotVideo.objects.all().order_by('-created')
    serializer_class = OpenEyesHotVideoSerializer
    # def list(self, request, *args, **kwargs):
    #     return CustomResponse(code=1,data=[],msg='lalala')


class DYHotVideoViewSet(CustomReadOnlyViewSet):
    queryset = DYHotVideoModel.objects.all().order_by('-created')
    serializer_class = DYHotVideoSerializer


class LSPHotVideoViewSet(CustomReadOnlyViewSet):
    queryset = LSPHotVideoModel.objects.all().order_by('-created')
    serializer_class = LSPHotVideoSerializer
