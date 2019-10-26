import os

# SECRET_KEY = os.urandom(24)
SECRET_KEY = "fvsjfguiergjdsfbvweknasf"
# CSRF可用保护机制
CKEDITOR_ENABLE_CSRF = True


DEBUG = True

SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/forum"
SQLALCHEMY_TRACK_MODIFICATIONS = False


# 发送者邮箱的服务器地址
MAIL_SERVER = "smtp.qq.com"

# MAIL_USE_TLS:端口号587
# MAIL_USE_SSL:端口号465
# QQ邮箱不支持非加密方式发送邮件
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USE_SSL = False
MAIL_USERNAME = "599663430@qq.com"
# 邮箱的授权码
MAIL_PASSWORD = "fmrlsciykefsbbha"
MAIL_DEFAULT_SENDER = "599663430@qq.com"


# Redis数据库配置
CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = ''
CACHE_REDIS_PASSWORD = ''


# 富文本编辑器的配置
CKEDITOR_FILE_UPLOADER = "upload"
