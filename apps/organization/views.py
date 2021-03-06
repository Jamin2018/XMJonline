from django.shortcuts import render, HttpResponse

from django.views.generic import View

from .models import CourseOrg, CityDict,Teacher
from operation.models import UserFavorite

# 分页
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserAskForm
from courses.models import Course
from django.db.models import Q

# from XMJonline.settings import MEDIA_URL   #在setting中配置好了
# Create your views here.

class OrgView(View):
    '''
    课程机构首页
    '''

    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()

        hot_orgs = all_orgs.order_by('-click_nums')[:3]



        # 设置全局课程搜索关键词
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) )

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 取出筛选机构
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 学习人数和课程数排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 3, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
            # 'MEDIA_URL':MEDIA_URL, #在setting中配置好了
        })


class AddUserAskView(View):
    '''
    用户咨询
    '''

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            # return HttpResponse("{'status':'success'}", content_type='application/json')  #双引号在外面会传递不过去
            return HttpResponse('{"status":"success"}', content_type='application/json')  # 一定要这样写
        else:
            # return HttpResponse("{'status':'fail','success':'咨询出错'}",content_type='application/json')  #双引号在外面会传递不过去
            return HttpResponse('{"status":"fail","msg":"咨询出错"}', content_type='application/json')  # 一定要这样写


class OrgHomeView(View):
    '''
    机构首页
    '''

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        #点击数加一
        course_org.click_nums +=1
        course_org.save()
        #判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        all_courses = course_org.course_org.all()[:8]
        all_teachers = course_org.org.all()[:5]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav,
        })


class OrgCourseView(View):
    '''
    机构课程列表
    '''

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        all_courses = course_org.course_org.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    '''
    机构介绍
    '''

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    '''
    机构教师列表
    '''

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        all_teachers = course_org.org.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    '''
    用户收藏，用户取消收藏
    '''

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        # 查询用户是否收藏过
        exit_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exit_records:
            #若已经存在，则去掉记录
            exit_records.delete()
            #机构收藏数减1
            if int(fav_type) == 3:
                teacher_nums = Teacher.objects.get(id=int(fav_id))
                teacher_nums.fav_nums -=1
                # 避免负数
                if teacher_nums.fav_nums < 0:
                    teacher_nums.fav_nums = 0
                teacher_nums.save()

            if int(fav_type) == 2:
                org_nums = CourseOrg.objects.get(id=int(fav_id))
                org_nums.fav_nums -=1
                # 避免负数
                if org_nums.fav_nums < 0:
                    org_nums.fav_nums = 0
                org_nums.save()

            if int(fav_type) == 1:
                course_nums = Course.objects.get(id=int(fav_id))
                course_nums.fav_nums -=1
                # 避免负数
                if course_nums.fav_nums < 0:
                    course_nums.fav_nums = 0
                course_nums.save()

            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav = UserFavorite.objects.create(user=request.user,
                                                       fav_id=int(fav_id),
                                                       fav_type=int(fav_type))
                # 机构收藏数加1
                if int(fav_type) == 3:
                    teacher_nums = Teacher.objects.get(id=int(fav_id))
                    teacher_nums.fav_nums += 1
                    teacher_nums.save()

                if int(fav_type) == 2:
                    org_nums = CourseOrg.objects.get(id=int(fav_id))
                    org_nums.fav_nums += 1
                    org_nums.save()
                if int(fav_type) == 1:
                    course_nums = Course.objects.get(id=int(fav_id))
                    course_nums.fav_nums += 1
                    course_nums.save()

                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    '''
    课程讲师列表页
    '''
    def get(self,request):
        all_teachers = Teacher.objects.all()


        # 设置全局课程搜索关键词
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(work_company__icontains=search_keywords) |
                                               Q(work_position__icontains=search_keywords) )

        # 人气讲师排序
        sort = request.GET.get('sort', '')

        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')


        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 3, request=request)
        teachers = p.page(page)

        return render(request,'teachers-list.html',{
            'all_teachers':teachers,
            'sorted_teachers':sorted_teachers,
            'sort':sort,
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        #点击数加一
        teacher.click_nums +=1
        teacher.save()

        all_courses = teacher.course_set.all()
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        #判断是否收藏
        has_teacher_faved = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=teacher.id,fav_type=3):
                has_teacher_faved = True

        has_org_faved = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_org_faved = True
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'all_courses':all_courses,
            'sorted_teachers': sorted_teachers,
            'has_org_faved':has_org_faved,
            'has_teacher_faved':has_teacher_faved
        })