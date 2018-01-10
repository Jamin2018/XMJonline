from random import Random

from users.models import EmailVerifyRecord

def random_str(randomlength=8):
    '''
    随机生成字符串
    '''
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def send_register_email(email,send_type='register'):
    '''
    email: 用户的邮箱
    type:验证码类型
    思路：将验证码加密加入到url链接中，用户点击链接，后端接受链接值并提取其中的加密的验证码，通过对比数据库中的数据判断
    '''
    # email_record = EmailVerifyRecord()
    code = random_str(16)
    # email_record.code = code
    # email_record.email = email
    # email_record.send_type = send_type
    EmailVerifyRecord.objects.create(code=code,email=email,send_type=send_type)

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'XMJ在线学习平台注册链接'
        email_body = '点击下面的链接激活该账号 ：http://127.0.0.1:8000/active/{0}'.format(code)
        #使用django内置函数发送邮件
        from django.core.mail import send_mail  #需要配置发送者
        from XMJonline.settings import EMAIL_FROM
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        return send_status

    if send_type == 'forget':
        email_title = 'XMJ在线学习平台密码重置链接'
        email_body = '点击下面的链接重置你的密码 ：http://127.0.0.1:8000/reset/{0}'.format(code)
        # 使用django内置函数发送邮件
        from django.core.mail import send_mail  # 需要配置发送者
        from XMJonline.settings import EMAIL_FROM
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        return send_status