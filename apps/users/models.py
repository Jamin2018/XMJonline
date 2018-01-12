from datetime import datetime

from django.db import models

# 扩展默认的auth_user表的字段类型
from django.contrib.auth.models import AbstractUser


# Create your models here.

# 扩展默认的auth_user表的字段类型
class UserProfile(AbstractUser):
    '''
    用户信息，继承了基础用户表
    '''
    nick_name = models.CharField(max_length=50,verbose_name=u'昵称',default=u'')
    birthday = models.DateField(verbose_name=u'生日',null=True,blank=True) #blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填，比如 admin 界面下增加 model 一条记录的时候。直观的看到就是该字段不是粗体
    gender = models.CharField(max_length=7,choices=(('male',u'男'),('female',u'女')),default='female')
    address = models.CharField(max_length=100,default=u'')
    mobile = models.CharField(max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to='image/%Y/%m',default=u'image/default.png',max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    #将用户未读信息数量放到request.user表中，这样不管什么页面都有这个数据
    def unread_nums(self):
        #获取用户未读消息数量
        from operation.models import UserMessage   #这个一定要放在这里，防止循环引入bug
        return UserMessage.objects.filter(user=self.id).count()


    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    '''
    邮箱验证码
    用于找回密码和注册
    '''
    code = models.CharField(max_length=20,verbose_name=u'验证码')
    email = models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type= models.CharField(choices=(('register',u'注册'),('forget',u'找回密码'),('update_email',u'修改邮箱')),max_length=20,verbose_name=u'验证码类型')
    send_time = models.DateTimeField(default=datetime.now,verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)

class Banner(models.Model):
    '''
    用户课程轮播图
    '''
    title = models.CharField(max_length=100,verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m',verbose_name='轮播图',max_length=100)
    url = models.URLField(max_length=200,verbose_name=u'访问地址')
    index = models.IntegerField(default=100,verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now,verbose_name= u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name