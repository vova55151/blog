from . import views
from .views import *
from django.urls import path, include, re_path
from django.urls import include, path
from rest_framework import routers

app_name = 'rest'
router = routers.DefaultRouter()

urlpatterns = [
    path('api/v1/', include([
        path('list/', ArticleList.as_view(), name='home'),
        path('create/', ArticleCreate.as_view(), name='create'),
        path('profile/', UserDetailView.as_view(), name='user_detail'),
        path('profile/update/', UserUpdateView.as_view(), name='user_update'),
        path('<str:slug>/', include([

            path('update/', ArticleUpdate.as_view(), name='update'),
            path('detail/', ArticleDetail.as_view(), name='detail'),
            path('delete/', ArticleDelete.as_view(), name='delete'),
            path('fav/', FavouritesAddView.as_view(), name='favourite'),
            path('comment/', CommentCreateView.as_view(), name='comment'),
            path('add_images/', ImageCreateView.as_view(), name='add_images'),
            path('comment/', CommentCreateView.as_view(), name='comment'),

        ])),
        path('<int:pk>/sub/', SubscribersAdd.as_view(), name='subscribe'),

    ])),


    path('', include(router.urls)),

]


