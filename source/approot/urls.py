"""approot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from metatask import views
#from django.shortcuts import render,render_to_response

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/666', view=lambda e: HttpResponse('戏说不是胡说')),
    path('register', views.register),
    path('login', views.login),
    path('getUserInformation', views.getUserInformation),
    path('uploadHeadImg', views.uploadHeadImg),
    path('getHeadImg', views.getHeadImg),
    path('getGroupInformation', views.getGroupInformation),
    path('modifyUserInformation', views.modifyUserInformation),

]
