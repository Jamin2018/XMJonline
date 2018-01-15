import json

from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect

from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate,login,logout  #django自带认证模块

#注册用户时候保存密码加密问题
from django.contrib.auth.hashers import make_password

# Create your views here.

#基于django用户登录认证模块，定义可以邮箱，手机登录等方式
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerifyRecord
from django.db.models import Q

from django.views.generic.base import View

from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UserInfoForm

#邮箱注册
from utils.email_send import send_register_email

from utils.mixin_utils import LoginRequiredMixin

from operation.models import UserCourse,UserFavorite,UserMessage

from organization.models import CourseOrg,Teacher
from courses.models import Course

# 分页
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Banner



class IndexView(View):
    '''
    首页
    '''
    def get(self,request):
        # 取轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 非广告位课程
        courses = Course.objects.all().filter(is_banner=False)[:6]
        # 广告位课程
        banner_courses = Course.objects.all().filter(is_banner=True)[:3]
        # 机构数量
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs,
        })



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
    '''
    用户登出
    '''
    def get(self,request):
        logout(request)
        # return render(request,'index.html')  #不能这么做，要重定向，为什么一定要重定向？
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


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
                    return HttpResponseRedirect(reverse('index'))
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

            user_profile = UserProfile.objects.create(email=email,password=make_password(password),username=email,is_active= False)
            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册！'
            user_message.save()
            #发送邮箱激活链接
            send_status = send_register_email(email,'register')
            if send_status:
                return render(request, 'login.html')
            else:
                return render(request, 'register.html', {'msg': '邮箱验证发送失败，请确保该邮箱是否有效。','register_form':register_form})
        else:
            return render(request, 'register.html', {'register_form':register_form})


class ActiveView(View):
    '''
    用户激活链接
    '''
    def get(self,request,code):
        all_records = EmailVerifyRecord.objects.filter(code=code).order_by('-send_time')
        if all_records:
            record = all_records[0]
            UserProfile.objects.filter(email=record.email).update(is_active=True)  # 激活状态
            return render(request, 'login.html')
        else:
            return render(request, 'login.html',{'msg':'该链接无效'})


class ResetView(View):
    '''
    获得重设密码页面
    '''
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
    '''
    密码重设确认
    '''
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
    '''
    重设密码请求
    '''
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


class UserInfoView(LoginRequiredMixin,View):
    '''
    个人信息
    '''
    def get(self,request):
        return render(request,'usercenter-info.html')

    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)  # 将整个USER实例传进去，类似上下文吧
        if user_info_form.is_valid():
            user_info_form.save()  # 因为上面的“上下文”，所以直接用ModelForm的特性直接保存数据
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class ImageUploadView(LoginRequiredMixin,View):
    '''
    用户修改头像
    '''
    # #第一种
    # def post(self,request):
    #     image_form = UploadImageForm(request.POST,request.FILES)   #因为文件是放在FILES中
    #     if image_form.is_valid():
    #         image = image_form.cleaned_data['image']   #所有通过验证的字段的值都在cleaned_data中
    #         request.user.image = image
    #         request.user.save()
    #     return render(request,'usercenter-info.html',{ })
    #第二种
    def post(self,request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)  # 将整个USER实例传进去，类似上下文吧
        if image_form.is_valid():
            image_form.save()   # 因为上面的“上下文”，所以直接用ModelForm的特性直接保存数据
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin,View):
    '''
    个人中心修改密码
    '''
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    '''
    个人中心发送邮箱验证码
    '''
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_status = send_register_email(email, 'update_email')
        if send_status:
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failure"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    '''
    个人中心中修改个人邮箱
    '''
    def post(self,request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin,View):
    '''
    我的学习课程
    '''

    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_courses':user_courses,
        })


class MyFavOrgView(LoginRequiredMixin,View):
    '''
    我的收藏的机构
    '''

    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            'org_list':org_list,
        })

class MyTeacherView(LoginRequiredMixin, View):
    '''
    我的收藏的老师
    '''

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })



class MyFavCourseView(LoginRequiredMixin, View):
    '''
    我的收藏的课程
    '''

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list':course_list,
        })


class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        #清空未读信息的标记改为已读消息
        all_unread_messages = UserMessage.objects.filter(has_read=False,user=request.user.id)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 3, request=request)
        messages = p.page(page)


        return render(request,'usercenter-message.html',{
            'all_messages':messages,
        })


def page_not_found(request):
    '''
    全局处理404页面

    '''
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response


def page_error(request):
    '''
    全局处理500页面

    '''
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response
