"""Bazar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views
#below for MEDIA file
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home , name='home'),
    #let include store url first traffic will come here and then we will handle in store url's :)
    path('store/',include('store.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
