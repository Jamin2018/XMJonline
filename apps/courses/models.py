from datetime import datetime

from django.db import models

from organization.models import CourseOrg,Teacher

# #富文本字段
# from DjangoUeditor.models import UEditorField

# Create your models here.


class Course(models.Model):
    '''
    课程基本信息
    '''
    course_org = models.ForeignKey(CourseOrg,verbose_name=u'课程机构',null=True,blank=True,related_name='course_org')
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    # detail = UEditorField(verbose_name=u"课程详情",width=600, height=300, imagePath="courses/ueditor/",
    #                                      filePath="courses/ueditor/", default='')
    detail = models.TextField(verbose_name=u'课程详情')
    is_banner = models.BooleanField(default=False,verbose_name=u'是否轮播')
    teacher = models.ForeignKey(Teacher,verbose_name=u'讲师',null=True,blank=True)
    degree = models.CharField(choices=(('cj',u'初级'),('zj',u'中级'),('gj',u'高级')),max_length=2,verbose_name=u'难度')
    learn_times = models.IntegerField(default=0,verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name=u'课程封面图',max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    category = models.CharField(max_length=20,verbose_name=u'课程类别',default='')
    tag = models.CharField(default='',verbose_name=u'课程标签',max_length=20)
    need_know = models.CharField(max_length=300,verbose_name=u'课程须知',default='')
    teacher_tell = models.CharField(max_length=300,verbose_name=u'老师告知',default='')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    #自定义获取章节数
    def get_zj_nums(self):
        '''
        获取课程章节数
        '''
        all_lessons = self.course.all().count()
        return all_lessons
    get_zj_nums.short_description = '章节数'   # 后台管理显示的title

    # 后台管理获得跳转链接
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</a>")
    go_to.short_description = '跳转'   # 后台管理显示的title


    # 自定义获取用户
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    # 自定义获取湛江详情
    def get_course_lesson(self):
        return self.course.all()[:5]

    def get_course_resource(self):
        return self.courseresource_set.all()

    def __str__(self):
        return self.name


# #后台系统根据布尔值BooleanField显示2张表，没成功
# class BannerCourse(Course):
#     class Meta:
#         verbose_name = '轮播课程'
#         verbose_name_plural = verbose_name
#
#         #关键参数
#         proxy = True



class Lesson(models.Model):
    '''
    章节详情
    '''
    course = models.ForeignKey(Course,verbose_name=u'课程',related_name='course')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    #自定义获取章节视频
    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name

class Video(models.Model):
    '''
    章节视频
    '''
    lesson = models.ForeignKey(Lesson,verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名称')
    url = models.CharField(max_length=200,verbose_name=u'访问地址',default='')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseResource(models.Model):
    '''
    章节资源
    '''
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m',verbose_name=u'资源文件',max_length=100)
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name