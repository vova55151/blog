from . import views
from .views import *
from django.urls import path, include, re_path
from django.urls import include, path
from rest_framework import routers

app_name = 'rest'
router = routers.DefaultRouter()



urlpatterns = [
    path('api/v1/list', ArticleView.as_view()),
    path('api/v1/update/<str:slug>', ArticleUpdateView.as_view()),
    path('api/v1/detail', ArticleDetailView.as_view()),
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

