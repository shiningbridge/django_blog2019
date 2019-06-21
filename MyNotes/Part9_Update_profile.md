## 第九部分 update profile

学习点：
* update profile
* resize the figure using Pillow

### 用form去update
users/forms.py
```python
...
from .models import Profile
...
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
```
* 先不让他们改密码的。。。。
* ?? forms.py是不是model的一个延伸。。。？？延伸model做的数据操作。而model单纯做数据的结构，存储。


#### template里：profile.html
把两个form放一起。。
```html
<form method="POST" enctype="multipart/form-data">  <!-- 这个encodeing是保证图片可以正常存储的  -->
          {% csrf_token %}                <!-- csrf token 增加安全性用的。。。 -->
          <fieldset class="form-group">
              <legend class="border-bottom mb-4">Profile info</legend>
              <!--  
              更进一步，可以用pipe ’|‘ 把crispy_form功能加进来-->
              {{ u_form | crispy }}
              {{ p_form | crispy }}
          </fieldset>
          <div class="form-group">
              <button class="btn btn-outline-info" type="submit">Update</button>
          </div>
      </form>

```
把两个form摞起来。。。
注意： `enctype="multipart/form-data"` encodeing是保证图片可以正常存储的.


#### 进一步改views

```python
@login_required ## decoration,加入条件，如果不满足，走另一条路，这里会跳转到login
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm( request.POST, 
                                    request.FILES, 
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Profile has been updated!')
            # return redirect('profile')    ## 直接跳转。
    else:
        u_form = UserUpdateForm(instance=request.user)  ## 自动填入当前的User，或者Profile的内容
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)
```
* Form 里传入 instance，他就可以操作了。
* 前边加入`request.POST`，则可以把POST内容更新进instance里边去。
    - 当然里边还不仅仅是POST。FILES也可以被更新，只要传进来。例如`request.FILES`
* 像之前register注册的交互验证一样。可以用 `.is_valid()`方法判断表格格式
    - 保存后，instance的更新被保存到数据库。
    - 跳转: 是著名的post get redirect pattern. 

##### 著名的post-get-redirect pattern.
如果不跳转，submit form post 之后，如果再Reload page, 浏览器会告警 warning "你确认要reload，因为data会被重新发送"
e.g.
```
The page that you're looking for used information that you entered. Returning to that page might cause any action you took to be repeated. Do you want to continue?
```
这是因为reload 会让你再次发 post request。 为了避免，我们在条件句内提前return 跳转。 就不会进入最尾部的 render -- 造成reload的效果了。

#### resize image for the profile
models.py, 在Profile model里，重写`save()`方法
```python
from PIL import Image
...
    def save(self):     ## overwrite
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
```
用Pillow带的`thumbnail`方法resize
