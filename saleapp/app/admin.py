from flask_admin.contrib.sqla import ModelView

from app import app, db
from flask_admin import Admin
from flask_admin.contrib import sqla

admin = Admin(app=app, name='eCommerce Admin', template_mode='bootstrap4')




