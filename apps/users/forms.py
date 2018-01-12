from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
    )
    password = forms.CharField(
        required=True,
        min_length=6,
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6,)
    captcha = CaptchaField(
        error_messages={"invalid":u'验证码错误'}
    )


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(
        error_messages={"invalid":u'验证码错误'}
    )


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=6,
                                error_messages={"min_length": u'最小输入6个字符'})
    password2 = forms.CharField(required=True,min_length=6,)


# 专门处理头像上传
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


# 专门处理头像上传
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','gender','birthday','address','mobile']