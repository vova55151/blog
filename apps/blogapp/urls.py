
from .views import *
from django.urls import path, include, re_path
app_name = 'blogapp'


urlpatterns = [
    path('', ArticleListView.as_view(model=Article), name='home'),
    path('create/', ArticleCreateView.as_view(),name='create'),
    path('<str:slug>/', include([

        path('update/', ArticleUpdateView.as_view(), name='update'),
        path('detail/', ArticleDetailView.as_view(), name='detail'),
        path('delete/', ArticleDeleteView.as_view(), name='delete'),
    ])),
]
