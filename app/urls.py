# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from django.conf.urls import  include
from app import views
from django.urls import re_path as url
urlpatterns = [

    # The home page
    url('', views.index, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
  

    # Matches any html file
   

]
