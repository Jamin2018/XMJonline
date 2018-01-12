from django.conf.urls import url

from .views import CourseListView,CourseDetailView,CourseInfoView,CourseCommentView,AddCommentView,LessonPlayView

urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$',CourseInfoView.as_view(),name='course_info'),
    #课程评论
    url(r'^comment/(?P<course_id>\d+)/$',CourseCommentView.as_view(),name='course_comment'),
    url(r'^add_comment/$',AddCommentView.as_view(),name='add_comment'),
    #课程播放
    url(r'^lesson_play/(?P<video_id>\d+)/$',LessonPlayView.as_view(),name='lesson_play'),
]