import re

from django import forms
from operation.models import UserAsk

# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True,min_length=2,max_length=20)
#     mobile = forms.CharField(required=True,min_length=11,max_length=11)
#     course_name = forms.CharField(required=True,min_length=5,max_length=50)


#类似DRf的序列化serializers表单
#下面的功能跟上面的一样
class UserAskForm(forms.ModelForm):
    # new_fields = forms.CharField(required=True)   #可继承字段并新增字段
    class Meta:
        model = UserAsk
        # fields = "__all__"  # 取全部字段
        fields = ('name', 'mobile', 'course_name', )  # 指定字段

    #还可以定义自动保存到数据库，自动调用save方法。

    #自定义mobile字段验证
    def clean_mobile(self):
        '''
        验证手机号码是否合法
        '''
        mobile = self.cleaned_data['mobile']
        #正则匹配手机号码
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        #失败抛出自定义失败信息
        else:
            raise forms.ValidationError(u'手机号码非法',code='mobile_invalid')