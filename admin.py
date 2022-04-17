from tkinter.tix import Tree
from flask import redirect,url_for,request
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin.base import expose

class AdminModelView(ModelView):
    can_create = True # production ce biti False
    can_export = True
    can_view_details = True
    column_export_exclude_list = ['password','avatar','is_admin']
    column_exclude_list = ['password']
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin == 1:          
            return True
        
    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated or current_user.is_admin == 0:
            return redirect(url_for('views_blueprint.home',next=request.url))


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("admin/index.html")

    def is_accessible(self):
            return current_user.is_authenticated and current_user.is_admin == 1

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated or current_user.is_admin == 0:
            return redirect(url_for('views_blueprint.home',next=request.url))