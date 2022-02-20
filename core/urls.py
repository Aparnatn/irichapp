# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.conf import settings
from django.urls import re_path as url
from django.conf.urls.static import static
from django.urls import path,include
from rest_framework import routers
from authentication import views
router = routers.DefaultRouter()  # add this
from authentication.views import (get_books)
                             
from django.urls import path
from authentication import views


urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("authentication.urls")), # Auth routes - login / register
    path("", include("app.urls")),
    url(r'getbooks', include(router.urls)),
    # path('index', views.index, name='index'),
   
    
  
    # path('homepage', HomepageView.as_view(), name='homepage'),

    # path('bills/', BillListView.as_view(), name='bills_view'),
    # path('payroll/', PayrollListView.as_view(), name='payroll_view'),
    # path('expenses/', ExpensesListView.as_view(), name='expenses_view'),
    # path('reports/', report_view, name='reports_view'),    # UI Kits Html files
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
