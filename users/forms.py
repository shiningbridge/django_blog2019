###
# Created Date: Monday June 17th 2019
# Author: Kangqiao
# -----
# Last Modified: 2019-06-18 00:20:08
# Modified By: the developer formerly known as Kangqiao at <zhaokangqiao@gmail.com>
# -----
# Copyright (c) 2019 NanFei
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
###

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  ## 定制其他field

    ## 这个是干嘛的呢？？？？
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

