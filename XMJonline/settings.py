"""
Django settings for XMJonline project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
#将apps目录加入到根目录，防止不通过pycharm运行就报错的问题(解决在cmd单独运行就报错的问题)
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#将apps目录加入到根目录，防止不通过pycharm运行就报错的问题(解决在cmd单独运行就报错的问题)
sys.path.insert(0,BASE_DIR)
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@=*9xh*8ur)*4xlmqh-megma=p48ejr%#%cvi1+s5mt!0^4v!o'

# SECURITY WARNING: don't run with debug turned on in production!
#
# # 项目上线，生产模式设置False
# DEBUG = False
#
# ALLOWED_HOSTS = ['*']

# 项目没上线
DEBUG = True

ALLOWED_HOSTS = []



# Application definition

#基于django用户登录认证模块，定义可以邮箱，手机登录等方式
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'courses',
    'organization',
    'operation',
    #xadmin后台管理
    'xadmin',
    'crispy_forms',
    'reversion',
    #验证码
    'captcha',
    #分页
    'pure_pagination',
    #富文本编辑
    'DjangoUeditor'
]

#分页
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

# 扩展默认的auth_user表的字段类型
# 用自定义UserProfile替换auth_user
AUTH_USER_MODEL = 'users.UserProfile'


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'XMJonline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media'   # 前端中全局的使用 {{ MEDIA_URL }}
            ],
        },
    },
]

WSGI_APPLICATION = 'XMJonline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xmjonline',
        'USER': 'root',
        'PASSWORD': 'q8850063',
        'HOST': '127.0.0.1',
        'OPTIONS':{"init_command":"SET foreign_key_checks = 0;", }
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

#使用django内置函数发送邮件，配置发送者
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '389098898@qq.com'
EMAIL_HOST_PASSWORD = 'embklxgffcndcbbj'
EMAIL_USE_TLS = True
EMAIL_FROM = '389098898@qq.com'

#文件上传
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# #项目上线后，static路径需要重新配置
# STATIC_ROOT = os.path.join(BASE_DIR,'static')