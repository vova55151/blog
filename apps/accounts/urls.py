from django.urls import path

from apps.accounts.views import *

app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('fav/<str:slug>/', favourite_add, name='favourite_add'),
    path('profile/fav/', favourite_list, name='favourite_list'),
    path('profile/<int:pk>', ProfileDetail.as_view(), name='pofile'),
    path('profile/<int:pk>/delete', ProfileDelete.as_view(), name='pofile_delete'),
    path('profile/<int:pk>/update', ProfileUpdate.as_view(), name='pofile_update'),
    path('profile/<int:pk>/sub', subscribers_add, name='subscribers_add'),
    path('profile/sublist', subscribers_list, name='subscribers_list'),
]
