"""blg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import ckeditor_uploader
import django
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
import django_registration.backends.activation.urls
from django.views.decorators.cache import never_cache
from django_registration.backends.activation.views import RegistrationView

from apps.accounts.forms import UserForm
from apps.accounts.views import SuccessRegistrationView, UserActivationView, UserRegistrationView
from blg import settings
from ckeditor_uploader import views
# TODO: локализация python manage.py makemessages -l 'ru' , python manage.py compilemessages
import ckeditor_uploader.urls
# TODO : sudo apt-get install gettext
ckeditor_urls = [
    re_path(r"^upload/", views.upload, name="ckeditor_upload"),
    re_path(
        r"^browse/",
        never_cache(views.browse),
        name="ckeditor_browse",
    ),
]
urlpatterns = [
    path('ckeditor/', include(ckeditor_urls)),
    path('i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += i18n_patterns(

    path('admin/', admin.site.urls),
    path('blog/', include('apps.blogapp.urls')),
    path('profile/', include('apps.accounts.urls')),
    path('accounts/register/', UserRegistrationView.as_view(), name='django_registration_register'),
    path('accounts/activate/complete/', SuccessRegistrationView.as_view(), name='django_registration_activated'),
    path('accounts/activate/<str:activation_key>/', UserActivationView.as_view(), name='django_registration_activate'),
    path('success_registration/', SuccessRegistrationView.as_view(), name='success_registration'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
