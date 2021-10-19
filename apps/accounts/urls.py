from django.urls import path

from apps.accounts.views import *
from apps.blogapp.views import UserArticleList, UserUpdateView, PasswordView
from django.contrib.auth import views as auth_view

app_name = 'accounts'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),  # TODO: переделелать
    path('fav/<str:slug>/', FavouritesAddView.as_view(), name='favourite_add'),
    path('fav/', FavList.as_view(), name='favourite_list'),
    path('', UserArticleList.as_view(), name='profile'),
    path('edit/', UserUpdateView.as_view(), name='profile-update'),
    path('pass_update/', PasswordView.as_view(),
         name='pass-update'),
    # path('<int:pk>/delete', ProfileDelete.as_view(), name='profile_delete'),
    path('<int:pk>/sub', SubscribersAdd.as_view(), name='subscribers_add'),
    path('sublist/', SubList.as_view(), name='subscribers_list'),
]
