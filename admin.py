from flask import redirect,url_for,request
from flask_admin import AdminIndexView
from forms import ProizvodForm,CenaForm
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import TemplateLinkRowAction
from flask_login import current_user
from flask_admin.base import expose
from config import db
from models import Cena, Proizvod
from proizvodi import kreiraj_proizvod,kreiraj_cenu,obrisi_proizvod

class AdminModelView(ModelView):
    can_create = False
    can_delete = False
    can_view_details = True
    column_export_exclude_list = ['password','avatar','is_admin']
    column_exclude_list = ['password']

class AdminModelViewCena(ModelView):
    can_create = False
    can_delete = True
    can_export = True
    can_view_details = True


class AdminModelViewProizvod(ModelView):
    can_create = False
    can_export = True
    can_view_details = True

    list_template = "admin/my_list.html"  # Override the default template
    column_extra_row_actions = [  # Add a new action button
        TemplateLinkRowAction("custom_row_actions.delete_row", "Delete Record"),
    ]
    
    @expose("/delete", methods=["POST"])
    def delete_view(self):
            product = dict(request.form)
            product_id = product['id']
            cena = Cena.query.filter_by(proizvod_id=product_id).first()
            if cena:
                obrisan = obrisi_proizvod(product_id=product_id,price_id=cena.price_id)
                if obrisan:
                    return super().delete_view()
            else:
                obrisan = obrisi_proizvod(product_id=product_id)
                if obrisan:
                    return super().delete_view()

            return redirect("/admin/proizvod")


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
            kreiraj_proizvod(name=form.naziv.data,description=form.opis.data,images=[form.img.data])
            return redirect('/admin/proizvod')
        return self.render('admin/kreiraj_proizvod.html',form=form)


    @expose("/kreiraj-cenu",methods=["GET","POST"])
    def kreiraj_cenu(self):
        form = CenaForm()
        proizvodi = Proizvod.query.all()
        izbor = [(proizvod.product_id,proizvod.naziv) for proizvod in proizvodi]
        form.product_id.choices = izbor
        if request.method == "POST" and form.validate_on_submit():
            kreiraj_cenu(cena=form.cena.data,currency=form.valuta.data.lower(),product_id=form.product_id.data)
            return redirect('/admin/cena')
        return self.render('admin/kreiraj_cenu.html',form=form)

    def is_accessible(self):
            return current_user.is_authenticated and current_user.is_admin == 1

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated or current_user.is_admin == 0:
            return redirect(url_for('views_blueprint.home',next=request.url))