from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from blueprints.views import views_blueprint
from blueprints.authentication import authentication_blueprint
from models import *
from config import db
from admin import AdminModelView,MyAdminIndexView

import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Najbolji3@localhost/webshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'darkly'

db.init_app(app)
migrate = Migrate(app,db)
login_manager = LoginManager()
login_manager.login_view = 'authentication_blueprint.prijava'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin = Admin(app,name='WebShop',template_mode='bootstrap3',index_view=MyAdminIndexView())
admin.add_view(AdminModelView(User,db.session))
admin.add_view(AdminModelView(Podaci,db.session))
admin.add_view(AdminModelView(Proizvod,db.session))


app.register_blueprint(views_blueprint)
app.register_blueprint(authentication_blueprint)


if __name__ == "__main__":
    app.run()