###
# Created Date: Saturday June 15th 2019
# Author: Kangqiao
# -----
# Last Modified: 2019-06-15 23:28:40
# Modified By: the developer formerly known as Kangqiao at <zhaokangqiao@gmail.com>
# -----
# Copyright (c) 2019 NanFei
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
###


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
]
