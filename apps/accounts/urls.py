from django.urls import path

from apps.accounts.views import *
from apps.blogapp.views import UserArticleList, UserUpdateView, PasswordView
from django.contrib.auth import views as auth_view

app_name = 'accounts'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', registration_view, name='register'),
    path('fav/<str:slug>/', favourite_add, name='favourite_add'),
    path('profile/fav/', favourite_list, name='favourite_list'),
    path('profile/', UserArticleList.as_view(), name='profile'),
    path('profile/update/', UserUpdateView.as_view(), name='profile-update'),
    path('profile/pass_update/', PasswordView.as_view(),
         name='pass-update'),
    path('profile/<int:pk>/delete', ProfileDelete.as_view(), name='profile_delete'),
    path('profile/<int:pk>/sub', subscribers_add, name='subscribers_add'),
    path('profile/sublist', subscribers_list, name='subscribers_list'),
]
