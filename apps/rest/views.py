from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, \
    RetrieveUpdateDestroyAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, get_object_or_404
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from apps.blogapp.models import Article, Image
from apps.blogapp.task import send_email
from apps.rest.permissions import ArticleAuthorAccessPermission
from apps.rest.serializers import UserSerializer, ImgSerializer, ArticleSerializerDetail, ArticleSerializerList, \
    CommentSerializer


class ArticleList(ListCreateAPIView):
    """
    Список статей
    """
    queryset = Article.objects.all().order_by('-name')
    serializer_class = ArticleSerializerList
    permission_classes = [permissions.IsAuthenticated]


class ArticleDetail(RetrieveAPIView):
    """
    Данные статьи
    """
    queryset = Article.objects.all().order_by('-name')
    serializer_class = ArticleSerializerDetail
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'


class ArticleCreate(CreateAPIView):
    """
    Создает статью,отправляет письма и добавляет автора
    """
    queryset = Article.objects.all().order_by('-name')
    serializer_class = ArticleSerializerDetail
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleUpdate(RetrieveUpdateDestroyAPIView):
    """
    Изменяет статью
    """
    queryset = Article.objects.all().order_by('-name')
    serializer_class = ArticleSerializerDetail
    permission_classes = [permissions.IsAuthenticated, ArticleAuthorAccessPermission]
    lookup_field = 'slug'


class ArticleDelete(DestroyAPIView):
    """
    Удаляет статью
    """
    queryset = Article.objects.all().order_by('-name')
    serializer_class = ArticleSerializerDetail
    permission_classes = [permissions.IsAuthenticated, ArticleAuthorAccessPermission]  # TODO:    "detail": "Метод
    # TODO:  \"GET\" не разрешен.","status_code": 405. Нужна ли эта вьюха?
    lookup_field = 'slug'


class FavouritesAddView(APIView):
    """
    Добавляет пост в избренное
    """
    serializer_class = ArticleSerializerDetail
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        post = get_object_or_404(Article, slug=kwargs['slug'])
        if post.favourites.filter(id=request.user.id).exists():
            post.favourites.remove(self.request.user)
        else:
            post.favourites.add(self.request.user)
        post.likes_count = post.favourites.count()
        post.save()
        return HttpResponseRedirect(reverse_lazy('blogapp:detail', kwargs={'slug': post.slug}))


class SubscribersAdd(APIView):
    """
    Подписывается на автора,если подписан - отписывается
    """
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, **kwargs):
        author = get_user_model().objects.get(pk=kwargs['pk'])
        if self.request.user != author:
            if author.subscribers.filter(pk=self.request.user.pk).exists():
                author.subscribers.remove(self.request.user)
            else:
                author.subscribers.add(self.request.user)
            author.save()
        return HttpResponseRedirect(reverse_lazy('blogapp:home'))


class UserUpdateView(RetrieveUpdateAPIView):
    """
    Класс для редактирования данных пользователя
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_object(self):
        return self.request.user


class UserDetailView(RetrieveAPIView):
    """
    Класс для просмотра данных пользователя
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ImageCreateView(CreateAPIView):  # TODO: вывести много форм?
    """
    Создание картинки
    """
    serializer_class = ImgSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(article=self.get_object())


class CommentCreateView(CreateAPIView):
    """
    Создание картинки
    """
    serializer_class = CommentSerializer
    queryset = Article.objects.all()
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(article=self.get_object(), author=self.request.user)
