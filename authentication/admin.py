# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from .models import *
from django.contrib import admin
admin.site.register(mobile)
admin.site.register(business_details)
admin.site.register(category)


from .models import  Transactions



 
admin.site.register(Transactions)
