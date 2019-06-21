###
# Created Date: Monday June 17th 2019
# Author: Kangqiao
# -----
# Last Modified: 2019-06-21 10:54:15
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
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  ## 定制其他field

    ## 这个是干嘛的呢？？？？
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()  

    ## 这个是干嘛的呢？？？？
    class Meta:
        model = User
        fields = ['username', 'email']  ## 不让改密码的先。

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
