"""XMJonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView

# from users.views import user_login
from users.views import LoginView,RegisterView,ActiveView,LogoutView,ForgetPwdView,ResetView,ModifyPwdView
from organization.views import OrgView

#处理静态文件
from django.views.static import serve
from XMJonline.settings import MEDIA_ROOT

import xadmin
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),

    url('^$',TemplateView.as_view(template_name='index.html'),name='index'), #处理静态文件？什么意思  这里的功能好像是不需要写视图函数，直接将index.html文件传到浏览器
    # url('^login/$',user_login,name='login'),
    url('^login/$',LoginView.as_view(),name='login'),
    url('^logout/$',LogoutView.as_view(),name='logout'),
    url('^register/$',RegisterView.as_view(),name='register'),

    url(r'^captcha/', include('captcha.urls')),
    #用户激活链接
    url(r'^active/(?P<code>.*)/$',ActiveView.as_view(),name='user_active'),
    #密码重置
    url(r'^reset/(?P<code>.*)/$',ResetView.as_view(),name='user_reset'),
    url(r'^modify_pwd/$',ModifyPwdView.as_view(),name='modify_pwd'),

    url(r'^forget/$',ForgetPwdView.as_view(),name='forget_pwd'),

    #课程机构url配置
    url(r'^org/', include('organization.urls',namespace='org')),
    # #课程机构首页
    # url(r'^org_list/$',OrgView.as_view(),name='org_list'),

    #处理media信息
    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT})

]
