from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()     ## 一步，就把user保存到数据库里了。
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('blog-home')    ## 直接跳转。
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error