from datetime import datetime

from django.db import models

# Create your models here.

class CityDict(models.Model):
    '''
    机构所属地
    '''
    name = models.CharField(max_length=20,verbose_name=u'城市')
    desc = models.CharField(max_length=200,verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseOrg(models.Model):
    '''
    机构详情
    '''
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    tag = models.CharField(default=u'世界名校',max_length=10,verbose_name=u'机构标签')
    category = models.CharField(max_length=20,choices=(('pxjg',u'培训机构'),('gx',u'高校'),('gr',u'个人')),verbose_name='机构类别',default='pxjg')
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏数')
    image = models.ImageField(upload_to='org/%Y/%m',verbose_name=u'logo',max_length=100)
    address = models.CharField(max_length=150,verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict,verbose_name=u'所在城市')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0,verbose_name=u'课程数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'机构详情'
        verbose_name_plural = verbose_name

    #自定义获取教师数量的方法
    def get_teachers_nums(self):
        return self.org.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    '''
    机构教师
    '''
    org = models.ForeignKey(CourseOrg,verbose_name=u'所属机构',related_name='org')
    name = models.CharField(max_length=50,verbose_name=u'教师名称')
    age = models.IntegerField(default=18, verbose_name=u'年龄')
    work_years = models.IntegerField(default=0,verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50,verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50,verbose_name=u'公司职位')
    points = models.CharField(max_length=50,verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name=u'头像', max_length=100,default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def get_course_nums(self):
        return self.course_set.all().count()

    def __str__(self):
        return self.name