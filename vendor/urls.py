# -*- coding:utf-8 -*-
from django.urls import path
from . import views
# from userapp.api.staticpage import StaticPageView

app_name = 'vendor'

urlpatterns = [
	path('', views.test, name='home'),
    ]
