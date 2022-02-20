# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import  re_path
from django.conf.urls import url, include
from app import views

urlpatterns = [

    # The home page
    url('', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
  

    # Matches any html file
   

]
