from django.shortcuts import render,HttpResponse

from django.contrib.auth import authenticate,login,logout  #django自带认证模块

#注册用户时候保存密码加密问题
from django.contrib.auth.hashers import make_password

# Create your views here.

#基于django用户登录认证模块，定义可以邮箱，手机登录等方式
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerifyRecord
from django.db.models import Q

from django.views.generic.base import View

from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm

#邮箱注册
from utils.email_send import send_register_email

class CustomBackend(ModelBackend):
    '''
    基于django用户登录认证模块，定义可以邮箱，手机登录等方式
    '''
    def authenticate(self,username = None, password = None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    def get(self,request):
        logout(request)
        return render(request,'index.html')


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)  # 成功返回user对象，失败返回None
            if user:
                # print('用户存在')
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '该邮箱未激活!'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误!'})
        else:
            return render(request, 'login.html', {'login_form':login_form})


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username','')
#         password = request.POST.get('password','')
#         user = authenticate(username=username,password=password)  # 成功返回user对象，失败返回None
#         if user:
#             # print('用户存在')
#             login(request,user)
#             return render(request,'index.html')
#         else:
#             return render(request,'login.html',{ 'msg':'用户名或密码错误'})
#     elif request.method == 'GET':
#         return render(request,'login.html')

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'msg': '该邮箱已经被使用','register_form':register_form})
            password = request.POST.get('password', '')
            UserProfile.objects.create(email=email,password=make_password(password),username=email,is_active= False)
            #发送邮箱激活链接
            send_status = send_register_email(email,'register')
            if send_status:
                return render(request, 'login.html')
            else:
                return render(request, 'register.html', {'msg': '邮箱验证发送失败，请确保该邮箱是否有效。','register_form':register_form})
        else:
            return render(request, 'register.html', {'register_form':register_form})


class ActiveView(View):
    def get(self,request,code):
        all_records = EmailVerifyRecord.objects.filter(code=code).order_by('-send_time')
        if all_records:
            record = all_records[0]
            UserProfile.objects.filter(email=record.email).update(is_active=True)
            return render(request, 'login.html')
        else:
            return render(request, 'login.html',{'msg':'该链接无效'})


class ResetView(View):
    def get(self,request,code):
        all_records = EmailVerifyRecord.objects.filter(code=code).order_by('-send_time')
        if all_records:
            record = all_records[0]
            email = record.email
            modify_form = ModifyPwdForm()
            return render(request, 'password_reset.html',{'email':email,'modify_form':modify_form})
        else:
            return render(request, 'login.html',{'msg':'该链接无效'})


class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'密码不一致'})
            UserProfile.objects.filter(email=email).update(password=make_password(pwd2))
            return render(request,'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})



class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                # 发送邮箱激活链接
                send_status = send_register_email(email, 'forget')
                if send_status:
                    return render(request, 'forgetpwd.html',
                                  {'msg': '邮件已发送，请点击邮件中的链接进行密码修改', 'forget_form': forget_form})
                else:
                    return render(request, 'forgetpwd.html',
                                  {'msg': '邮箱验证发送失败，请确保该邮箱是否有效', 'forget_form': forget_form})
            else:
                return render(request, 'forgetpwd.html', {'msg': '该邮箱不存在','forget_form': forget_form})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})