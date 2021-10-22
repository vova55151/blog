from django.contrib.auth.models import User, Group
from rest_framework import serializers

from apps.blogapp.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['name', 'descr', 'category', 'content', 'slug', 'preview', 'comments_count', 'likes_count']



