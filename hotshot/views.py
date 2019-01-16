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

from hotshot.models import Snippet, DailyVideo, HotVideo, UserFavorite, DYHotVideoModel, LSPHotVideoModel
from hotshot.permissions import IsOwnerOrReadOnly
from hotshot.serializers import SnippetSerializer, UserSerializer, DailyVideoSerializer, HotVideoSerializer, \
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


class UserRegister(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        return Response(data='', status=status.HTTP_400_BAD_REQUEST)
    

class DailyVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyVideo.objects.all()
    serializer_class = DailyVideoSerializer


class HotVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HotVideo.objects.all()
    serializer_class = HotVideoSerializer


class DYHotVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DYHotVideoModel.objects.all()
    serializer_class = DYHotVideoSerializer


class LSPHotVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LSPHotVideoModel.objects.all()
    serializer_class = LSPHotVideoSerializer
