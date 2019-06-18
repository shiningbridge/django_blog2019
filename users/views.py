from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()     ## 一步，就把user保存到数据库里了。
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created, ready for log in!')
            return redirect('login')    ## 直接跳转。
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error