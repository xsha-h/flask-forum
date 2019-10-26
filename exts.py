from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cache import Cache
from flask_ckeditor import CKEditor


db = SQLAlchemy()
mail = Mail()
cache = Cache()
ckeditor = CKEditor()
