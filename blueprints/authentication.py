from flask import Blueprint,render_template,redirect,url_for,flash,session
from forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
from models import User
from config import db
from flask_login import login_required,login_user,logout_user,current_user


authentication_blueprint = Blueprint("authentication_blueprint",__name__)


@authentication_blueprint.route("/prijava-registracija")
def prijava_registracija():
    if current_user.is_authenticated:
        return redirect(url_for('views_blueprint.home'))
    else:
        register_form = RegisterForm(prefix='register')
        login_form = LoginForm(prefix='login')
        return render_template('authentication/login_register.html',register_form=register_form,login_form=login_form)


@authentication_blueprint.route("/registracija",methods=["POST"])
def registracija():
    register_form = RegisterForm(prefix='register')
    if register_form.validate_on_submit():
            user_username = User.query.filter_by(username=register_form.username.data).first()
            user_email = User.query.filter_by(email=register_form.email.data).first()
            if user_username:
                register_form.username.data = ''
                flash('Korisnik već postoji! Pokušaj ponovno.',category='danger')
                return redirect(url_for('authentication_blueprint.prijava_registracija'))
                
            elif user_email:
                register_form.email.data = ''
                flash('Email već postoji! Pokušaj ponovno.',category='danger')
                return redirect(url_for('authentication_blueprint.prijava_registracija'))

            elif register_form.password.data != register_form.confirm_password.data:
                flash('Lozinke se ne poklapaju. Pokušaj ponovno.',category='danger')
                return redirect(url_for('authentication_blueprint.prijava_registracija'))

            else:
                hashed_password = generate_password_hash(register_form.password.data)
                user = User(email=register_form.email.data,username=register_form.username.data,password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash("Uspešna registracija!",'success')
                return redirect(url_for('authentication_blueprint.prijava_registracija'))    
        

@authentication_blueprint.route("/prijava",methods=["POST"])
def prijava():
    login_form = LoginForm(prefix='login')
    user = User.query.filter_by(username=login_form.username.data).first()
    if login_form.validate_on_submit():
        if user:
            if check_password_hash(user.password,login_form.password.data):
                login_user(user)
                flash("Uspešna prijava!",'success')
                return redirect(url_for('views_blueprint.home'))
            
        
    flash("Pogrešno korisničko ime ili lozinka! Pokušaj ponovno.",category='danger')        
    return redirect(url_for('authentication_blueprint.prijava_registracija'))

@authentication_blueprint.route("/admin")
def admin_dashboard():
    return render_template("admin/index.html")


@authentication_blueprint.route("/odjava")
@login_required
def odjava():
    logout_user()
    if 'korpa' in session:
        session.pop('korpa')

    if 'kolicina' in session:
        session['kolicina'].update({'kolicina':0})
            
    flash('Upravo ste se odjavili!',category='warning')
    return redirect(url_for('views_blueprint.home'))