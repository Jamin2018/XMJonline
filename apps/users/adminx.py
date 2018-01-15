import xadmin
#额外的主题修改
from xadmin import views

from .models import EmailVerifyRecord,Banner

# xadmin进阶配置,最新的已经不需要了
# from xadmin.plugins.auth import UserAdmin
# from .models import UserProfile
#
# class UserProfileAdmin(UserAdmin):
#     pass
#
# xadmin.site.register(UserProfile,UserProfileAdmin)

#全局设置
class GlobalSettings(object):
    site_title = 'XMJsystem'    #Logo
    site_footer = 'XMJ在线学习后台管理系统'   #网页页脚信息
    menu_style = 'accordion'    #右侧导航栏折叠功能


xadmin.site.register(views.CommAdminView,GlobalSettings)
#额外的主题修改
class BaseSetting(object):
    enable_themes = True    #表示使用主题功能
    use_bootswatch = True


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', "send_type",'send_time']
    #查询
    search_fields = ['code', 'email', "send_type"]
    #筛选(后台管理页面中的过滤器)
    list_filter = ['email', "send_type",'send_time']

    # 自定义后台系统的icon
    model_icon = 'fa fa-envelope-square'

class BannerAdmin(object):
    list_display = ['title', 'image', "url",'index','add_time']
    #查询
    search_fields = ['title', 'image', "url",'index']
    #筛选(后台管理页面中的过滤器)
    list_filter = ['title', 'image', "url",'index','add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
