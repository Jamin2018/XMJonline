from django.shortcuts import render,HttpResponse
from django.views.generic import View
# 分页
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course,Video
from operation.models import UserFavorite,CourseComments,UserCourse

# 验证有没有权限，即是否登录
from utils.mixin_utils import LoginRequiredMixin

from django.db.models import Q

# Create your views here.

class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = all_courses.order_by('-click_nums')[:3]

        # 设置全局课程搜索关键词
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords) )

        # 学习人数和热门课程排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')

        org_nums = all_courses.count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)


        return render(request,'course-list.html',{
            'all_courses':courses,
            'sort': sort,
            'hot_courses':hot_courses,
        })

class CourseDetailView(View):
    '''
    课程详情页
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        #增加点击数(用filter取到的是QuerySet对象，可以用updata,但是不好+1数据，用get取数据修改数据调用save（）方法更简单)
        course.click_nums +=1
        course.save()

        #通过tag字段取出相关课程
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        #判断是否已经学习过
        has_learn = False
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if user_courses:
            has_learn = True

        # 判断是否收藏
        course_org_has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                course_org_has_fav = True

        course_has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                course_has_fav = True
        return render(request,'course-detail.html',{
            'course':course,
            'relate_courses':relate_courses,
            'course_org_has_fav':course_org_has_fav,
            'course_has_fav':course_has_fav,
            'has_learn':has_learn,
        })


class CourseInfoView(LoginRequiredMixin,View):
    '''
    课程章节信息
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            UserCourse.objects.create(user=request.user,course=course)
            course.students +=1
            course.save()


        #该课程同学们还学过什么课程的功能
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        #取出所有用户的课程的对象
        user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids =  [user_course.course.id for user_course in user_courses]
        # 取出相关的课程对象
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]



        return render(request, 'course-video.html',{
            'course':course,
            'relate_courses':relate_courses,
        })

class CourseCommentView(LoginRequiredMixin, View):
    '''
    课程评论页面
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.filter(course_id=course_id)

        #该课程同学们还学过什么课程的功能
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        #取出所有用户的课程的对象
        user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids =  [user_course.course.id for user_course in user_courses]
        # 取出相关的课程对象
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-comment.html',{
            'course':course,
            'all_comments':all_comments,
            'relate_courses': relate_courses,
        })


class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if int(course_id) > 0 and comments:
            CourseComments.objects.create(user=request.user,course_id=course_id,comments=comments)
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')

class LessonPlayView(LoginRequiredMixin,View):
    '''
    视频播放页面
    '''
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        all_comments = CourseComments.objects.filter(course_id=video_id)

        # 该课程同学们还学过什么课程的功能
        user_courses = UserCourse.objects.filter(course=course)
        # 取出所有用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出所有用户的课程的对象
        user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程的id
        course_ids = [user_course.course.id for user_course in user_courses]
        # 取出相关的课程对象
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-play.html', {
            'course': course,
            'all_comments': all_comments,
            'relate_courses': relate_courses,
            'video':video,
        })

