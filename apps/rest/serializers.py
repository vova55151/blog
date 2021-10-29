from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from apps.blogapp.models import Article, Image


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['img', 'alt']


class ArticleSerializer(serializers.ModelSerializer):
    image_set = ImgSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['name', 'descr', 'category', 'content', 'slug', 'preview', 'image_set', 'comments_count',
                  'likes_count']

    # def create(self, validated_data):  # TODO : создавать картинки в отдельной вьюхе
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
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone', 'img', 'email']
