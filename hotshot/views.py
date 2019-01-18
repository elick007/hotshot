import uuid

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import mixins

from hotshot.base.restbase import CustomViewBase, CustomResponse, CustomReadOnlyViewSet
from hotshot.models import Snippet, OpenEyesDailyVideo, OpenEyesHotVideo, UserFavorite, DYHotVideoModel, LSPHotVideoModel, HotShotUser
from hotshot.permissions import IsOwnerOrReadOnly
from hotshot.serializers import SnippetSerializer, UserSerializer, OpenEyesDailyVideoSerializer, OpenEyesHotVideoSerializer, \
    UserFavoriteSerializer, DYHotVideoSerializer, LSPHotVideoSerializer
from rest_framework.parsers import JSONParser
from rest_framework import generics


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
        password_post = request.data['password']
        if ac == 'login':
            login_dict = HotShotUser.objects.filter(username=username_post, password=password_post)
            if login_dict.exists():
                data = {'uid': '%s' % login_dict[0].uid}
                return CustomResponse(code=1, msg='login success', data=data, status=status.HTTP_200_OK)
            return CustomResponse(code=0, msg='username or password error', status=status.HTTP_200_OK)
        if ac == 'register':
            register_dict = HotShotUser.objects.filter(username=username_post)
            if register_dict.exists():
                return CustomResponse(code=0, msg='username exist', status=status.HTTP_200_OK)
            else:
                uid = uuid.uuid1().int >> 90
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(uid=str(uid))
                    return CustomResponse(code=1, msg='register success', data='', status=status.HTTP_200_OK)
                return CustomResponse(code=0, msg='system error', data='')
        return CustomResponse(code=0, msg='key ac not right', data='')

    def get(self, request, format=None):
        return Response(None, status=status.HTTP_400_BAD_REQUEST)


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @action(detail=True)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserFavoriteView(generics.ListCreateAPIView):
    queryset = UserFavorite.objects.all()
    serializer_class = UserFavoriteSerializer


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
