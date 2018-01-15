import xadmin
from .models import Course,Lesson,Video,CourseResource   # BannerCourse

# 添加课程的时候外键关联该课程的数据直接添加编辑的设置
class LessonInline(object):
    model = Lesson
    extra = 0
# 添加课程的时候外键关联该课程的数据直接添加编辑的设置
class CourseResourceInline(object):
    model = CourseResource
    extra = 0

class CourseAdmin(object):
    import_excel = True

    inlines = [LessonInline,CourseResourceInline]

    # 数据展示
    list_display = ['name','desc','detail','degree','learn_times','students','get_zj_nums','go_to']

    # 查询
    search_fields = ['name','desc','detail','degree','students']

    # 筛选(后台管理页面中的过滤器)
    list_filter = ['name','desc','detail','degree','learn_times','students']

    # 自定义后台系统的icon
    model_icon = 'fa fa-location-arrow'  #这是第三方字体库，用最新的版本需要替换对应js和fonts文件

    # 后台自定义默认排序
    ordering = ['-click_nums']

    # 后台自定义字段只可读
    # readonly_fields = ['click_nums','fav_nums']
    readonly_fields = ['click_nums']

    # 后台自定义字段不显示
    exclude = ['fav_nums']   #这里会跟readonly_fields冲突，所以readonly_fields的fav_nums去掉了，

    # 后台自定义不是下拉选择框，而是搜索框（解决了为什么用户不是下拉框的问题。。）
    relfield_style = 'fk-ajax'

    # 后台直接在表上修改数据
    list_editable = ['degree','desc']

    # xadmin/plugins/refresh插件定时刷新页面
    refresh_times = [10,60]   # 后台可选择10秒刷新一次或者60秒刷新一次


    # 富文本显示
    style_fields = {'detail':'ueditor'}

    #
    # def post(self, request, *args, **kwargs):
    #     if 'excel' in request.FILES:
    #         pass
    #     return super(CourseAdmin,self).post(request, args, kwargs)

    # 跟下面一样没有成功
    # def save_models(self):
    #     # 在保存课程的时候统计课程机构的课程数
    #     obj = self.new_obj
    #     obj.save()
    #     if obj.course_org is not None:
    #         course_org = obj.course_org
    #         course_org.course_nums = Course.objects.filter(course_org=course_org).count()
    #         course_org.save()

## 后台系统根据布尔值BooleanField显示2张表，没成功
# class BannerCourseAdmin(object):
#     inlines = [LessonInline,CourseResourceInline]
#
#     # 数据展示
#     list_display = ['name','desc','detail','degree','learn_times','students']
#
#     # 查询
#     search_fields = ['name','desc','detail','degree','students']
#
#     # 筛选(后台管理页面中的过滤器)
#     list_filter = ['name','desc','detail','degree','learn_times','students']
#
#     # 过滤取出的数据
#     def queryset(self):
#         qs = super(BannerCourseAdmin, self).queryset()
#         qs.filter(is_banner = True)
#         return qs
#
# xadmin.site.register(BannerCourse,BannerCourseAdmin)


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