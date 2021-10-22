from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework import permissions

from apps.blogapp.models import Article
from apps.rest.serializers import ArticleSerializer


class ArticleView(ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('-name')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArticleUpdateView(RetrieveUpdateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('-name')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'


class ArticleDetailView(RetrieveAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('-name')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'