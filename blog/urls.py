###
# Created Date: Saturday June 15th 2019
# Author: Kangqiao
# -----
# Last Modified: 2019-06-22 22:36:24
# Modified By: the developer formerly known as Kangqiao at <zhaokangqiao@gmail.com>
# -----
# Copyright (c) 2019 NanFei
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
###


from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    ## PostDetailView默认会去找叫做 post_detail.html 的template
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),   ## 这里<pk>是convention，也是可以减少views里的代码。
    path('post/new/', PostCreateView.as_view(), name='post-create'),        ## 这里，PostCreateView会默认去找post_form.html的template
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),        ## 这里，一样
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),        ## 这里，一样
    path('about/', views.about, name='blog-about'),
]
