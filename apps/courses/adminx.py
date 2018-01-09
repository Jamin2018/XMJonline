import xadmin
from .models import Course,Lesson,Video,CourseResource

class CourseAdmin(object):
    list_display = ['name','desc','detail','degree','learn_times','students']
    search_fields = ['name','desc','detail','degree','students']
    list_filter = ['name','desc','detail','degree','learn_times','students']


class LessonAdmin(object):
    list_display = ['course','name','add_time']
    # 因为course是外键，过滤器需要指定详细的外键字段才能在前端正确显示并且使用
    search_fields = ['course__name','name']
    #因为course是外键，过滤器需要指定详细的外键字段才能在前端正确显示
    list_filter = ['course__name','name','add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson__name', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download','add_time']
    search_fields = ['course__name', 'name', 'download']
    list_filter = ['course__name', 'name', 'download','add_time']

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)