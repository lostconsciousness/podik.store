"""pods URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from main.views import heater, homepage, iqos, load_more, filter_data, novaPost, update_price, my_views, get_image, update_visibility, update_message
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('<int:tg_id>/', homepage, name="homepage"),
    path('heater/', heater, name="heater"),
    path('iqos/', iqos, name = "iqos"),
    path('admin/', admin.site.urls),
    path('load_more/', load_more, name = "load_more"),
    path('filter_data/', filter_data, name = "filter_data"),
    path('novaPost/', novaPost, name="novaPost"),
    path('update_price/<str:ids>/', update_price, name = 'update_price'),
    path('my_view/', my_views, name = "my_view"),
    path('update-price/', update_price, name='update_price'),
    path('update_visibility/', update_visibility, name = 'update_visibility'),
    path('image/', get_image, name='image'),
    path('update_message/', update_message, name = "update_message")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)