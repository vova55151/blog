from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from apps.blogapp.models import Article, Image, Comment


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['img', 'alt']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'rating']


class ArticleSerializerDetail(serializers.ModelSerializer):
    image_set = ImgSerializer(many=True, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['name', 'descr', 'category', 'content', 'slug', 'preview', 'image_set', 'comment_set',
                  'comments_count','likes_count']


class ArticleSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['name', 'descr', 'category', 'content', 'preview', 'comments_count',
                  'likes_count']

    # def create(self, validated_data):
    #     imgs = validated_data.pop('image_set')
    #     article = Article.objects.create(**validated_data)
    #     for img in imgs:
    #         Image.objects.create(article=article, **img)
    #     return article

    # def update(self, instance, validated_data):
    #     tracks_data = validated_data.pop('tracks')
    #     album = Album.objects.create(**validated_data)
    #     for track_data in tracks_data:
    #         Track.objects.create(album=album, **track_data)
    #     return album


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone', 'img', 'email']
