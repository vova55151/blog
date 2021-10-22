from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView

from apps.menu.models import TextPage


class TextPageView(DetailView):
    model = TextPage
    template_name = 'blogapp/text_page.html'
    query_pk_and_slug = True
