from flask import redirect,url_for,request
from flask_admin import AdminIndexView
from requests import session
from forms import ProizvodForm
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import TemplateLinkRowAction
from flask_login import current_user
from flask_admin.base import expose
from models import Proizvod
from config import db

class AdminModelView(ModelView):
    can_create = False
    can_delete = False
    can_edit = True
    can_view_details = True
    column_export_exclude_list = ['password','avatar','is_admin']
    column_exclude_list = ['password']


class AdminModelViewProizvod(ModelView):
    can_create = False
    can_export = True
    can_view_details = True
    column_exclude_list = ['img']

    list_template = "admin/my_list.html"
    column_extra_row_actions = [
        TemplateLinkRowAction("custom_row_actions.delete_row", "Delete Record"),
    ]
    
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

    @expose("/kreiraj-proizvod",methods=["GET","POST"])
    def kreiraj_proizvod(self):
        form = ProizvodForm()
        if request.method == "POST" and form.validate_on_submit():
            proizvod = Proizvod(naziv=form.naziv.data,opis=form.opis.data,cena_proizvoda=form.cena.data,valuta=form.valuta.data,img=form.img.data,dostupna_kolicina=form.dostupna_kolicina.data)
            db.session.add(proizvod)
            db.session.commit()
            return redirect('/admin/proizvod')
        return self.render('admin/kreiraj_proizvod.html',form=form)


    def is_accessible(self):
            return current_user.is_authenticated and current_user.is_admin == 1

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated or current_user.is_admin == 0:
            return redirect(url_for('views_blueprint.home',next=request.url))