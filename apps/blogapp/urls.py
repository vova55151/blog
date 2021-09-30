from django.urls import path
from .views import *

app_name = 'blogapp'

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('', ArticleListView.as_view(model=Article), name='home'),
    path('update/<str:slug>/', ArticleUpdateView.as_view(), name='update'),
    path('detail/<str:slug>/', ArticleDetailView.as_view(), name='detail'),
    path('delete/<str:slug>/', ArticleDeleteView.as_view(), name='delete'),
]
