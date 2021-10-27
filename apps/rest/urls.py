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

        ])),
        path('<int:pk>/sub/', SubscribersAdd.as_view(), name='subscribe'),


    ])),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),

]

# path('', ArticleListView.as_view(model=Article), name='home'),
# path('create/', ArticleCreateView.as_view(),name='create'),
# path('comment/<int:pk>/', CommentCreateView.as_view(),name='comment'),
# path('<str:slug>/', include([
#
#     path('update/', ArticleUpdateView.as_view(), name='update'),
#     path('detail/', ArticleDetailView.as_view(), name='detail'),
#     path('delete/', ArticleDeleteView.as_view(), name='delete'),
# ])),
