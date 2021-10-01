from django.urls import path

from apps.accounts.views import login_view, logout_view, registration_view, favourite_add, favourite_list

app_name = 'accounts'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('fav/<str:slug>/', favourite_add, name='favourite_add'),
    path('profile/fav/', favourite_list, name='favourite_list'),
]