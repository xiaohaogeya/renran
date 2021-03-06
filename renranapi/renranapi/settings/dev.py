"""
Django settings for renranapi project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'byi^m*b#9*n++=8sr)0bxqb!yj+t9)5)u4be(p^rn#v-1pa6m0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "api.renran.cn",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'xadmin',
    'crispy_forms',
    'reversion',
    'users',
    'home',
    'oauth',
    'article',
    'payments',
    'store',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'renranapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'renranapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "renran_user",
        "PASSWORD": "renran",
        "NAME": "renran",
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATECFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
# ???????????????????????????????????????[????????????]???
# ????????? uploads??????????????????????????????????????????????????????
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
# ?????????????????????url????????????
MEDIA_URL = "/media/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { # ?????????????????????
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # ????????????,???????????????,????????????????????????????????????
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/renran.log"),
            # ??????????????????????????????,??????????????????300M
            'maxBytes': 300 * 1024 * 1024,
            # ???????????????????????????,???????????????????????????10
            'backupCount': 10,
            # ????????????:????????????
            'formatter': 'verbose'
        },
    },
    # ????????????
    'loggers': {
        'django': { # ???????????????django?????????????????????????????????????????????django?????????????????????
            'handlers': ['console', 'file'],
            'propagate': True, # ???????????????????????????????????????????????????????????????
        },
    }
}



REST_FRAMEWORK = {
    # ????????????
    'EXCEPTION_HANDLER': 'renranapi.utils.exceptions.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}


CORS_ORIGIN_WHITELIST = (
    "http://www.moluo.net:8080",
)
CORS_ALLOW_CREDENTIALS = False

AUTH_USER_MODEL = 'users.User'



import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}

AUTHENTICATION_BACKENDS = [
    'users.utils.AccountModelBackend',
]

# ?????????????????????
TENCENT_CAPTCHA = {
    "GATEWAY": "https://ssl.captcha.qq.com/ticket/verify",
    "APPID": "2072894469",
    "App_Secret_Key": "0vcR-k9wMOk1SArX_gvB7qQ**",
}


# ??????redis??????
CACHES = {
    # ????????????
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # ???????????????,???????????????????????????
        "LOCATION": "redis://127.0.0.1:6379/0",

        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # ?????????xadmin??????admin???session??????
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # ???????????????????????????
    "sms_code":{
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# ??????xadmin???????????????,????????????session?????????redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# ????????????????????????
SMS = {
    "_accountSid": "8a216da87051c90f0170a4c069db2ba6",
    "_accountToken": "57e4b0d21f0c4603bfdd3f25d5550e3e",
    "_appId": "8a216da87051c90f0170a4c06a472bad",
    "_serverIP": "sandboxapp.cloopen.com",
    "_serverPort": "8883",
}

# QQ????????????
QQ_APP_ID = '101403367'
QQ_APP_KEY = '93112df14c10d6fde74baa62f5de95ab'
QQ_REDIRECT_URL = 'http://www.moluo.net:8080/oauth_callback.html'
QQ_STATE = "/" # ????????????????????????????????????????????????


# django????????????
DEFAULT_FILE_STORAGE = 'renranapi.utils.fastdfs.fdfs_storage.FastDFSStorage'

# FastDFS
FDFS_URL = 'http://192.168.0.109:8888/'  # ??????????????????????????? ip??????????????????????????????ip??????
FDFS_CLIENT_CONF = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')



ALIAPY_CONFIG = {
    # "gateway_url": "https://openapi.alipay.com/gateway.do?", # ???????????????????????????
    "gateway_url": "https://openapi.alipaydev.com/gateway.do?", # ???????????????????????????
    "appid": "2021001145609128",
    "app_notify_url": None,
    "app_private_key_path": os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem"),
    "alipay_public_key_path": os.path.join(BASE_DIR, "apps/payments/keys/alipay_public_key.pem"),
    "sign_type": "RSA2",
    "debug": False,
    "return_url": "http://www.moluo.net:8080/wallet", # ??????????????????
    "notify_url": "http://api.renran.cn:8000/payments/alipay/result/", # ??????????????????
}

# tablestore
OTS_ID = "LTAI4FoDWGkE35pb7yRvvQvo"
OTS_SECRET = "8UVdyQfVyKnFdbsjuWBOcLCiaezGjP"
OTS_INSTANCE = "xiaohaorenran"
OTS_ENDPOINT = "https://xiaohaorenran.cn-hangzhou.ots.aliyuncs.com"
