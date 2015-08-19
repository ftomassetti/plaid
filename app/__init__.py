from flask import Flask
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import SQLAlchemyUserDatastore
from flask.ext.security import Security

from config import configuration


app = Flask(__name__)
app.config.from_object(configuration)
try:
    app.config.from_object('local_settings')
except:
    pass
babel = Babel(app)
mail = Mail(app)
db = SQLAlchemy(app)


from app import forms
from app import models
from app import render
from app import views

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import User, Patch, Role, Submitter, Project, Comment, Series, Topic, Tag

admin = Admin(app, name='plaid')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Patch, db.session))
admin.add_view(ModelView(Submitter, db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Series, db.session))
admin.add_view(ModelView(Topic, db.session))
admin.add_view(ModelView(Tag, db.session))

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore,
                    register_form=forms.ExtendedRegisterForm)
