from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from apps.blogapp.models import Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['name', 'descr', 'category', 'content', 'slug', 'preview', 'comments_count', 'likes_count']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone', 'img', 'email']
