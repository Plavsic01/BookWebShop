from flask import Blueprint,url_for,render_template,redirect,flash
from werkzeug.security import generate_password_hash,check_password_hash
from forms import PodaciForm,PromenaLozinke
from models import User,Podaci
from flask_login import login_required,current_user
from config import db


user_blueprint = Blueprint("user_blueprint",__name__)


@user_blueprint.route('/korisnik')
@login_required
def korisnik_page():
    form_podaci = PodaciForm(prefix='podaci')
    form_promena = PromenaLozinke(prefix='promena')

    korisnik_podaci = Podaci.query.filter_by(user_id=current_user.id).first()

    form_podaci.email.data = current_user.email
    if korisnik_podaci is not None:
        form_podaci.ime.data = korisnik_podaci.ime
        form_podaci.prezime.data = korisnik_podaci.prezime
        form_podaci.broj_telefona.data = korisnik_podaci.broj_telefona
        form_podaci.ulica.data = korisnik_podaci.adresa
        form_podaci.kucni_broj.data = korisnik_podaci.broj_ulice
        form_podaci.grad.data = korisnik_podaci.grad
        form_podaci.postanski_broj.data = korisnik_podaci.postanski_broj
    return render_template('korisnik/korisnik.html',form_podaci=form_podaci,form_promena=form_promena)


@user_blueprint.route('/korisnik/izmeni',methods=['POST'])
@login_required
def izmeni_korisnik():
    form_podaci = PodaciForm(prefix='podaci')
    korisnik_podaci = Podaci.query.filter_by(user_id=current_user.id).first()
    
    if form_podaci.is_submitted():
        if korisnik_podaci is not None:
            korisnik_podaci.ime = form_podaci.ime.data
            korisnik_podaci.prezime = form_podaci.prezime.data
            korisnik_podaci.broj_telefona = form_podaci.broj_telefona.data
            db.session.commit()
            flash("Uspešno ažuriranje podataka!",'success')
        else:
            podaci = Podaci(ime=form_podaci.ime.data,prezime=form_podaci.prezime.data,broj_telefona=form_podaci.broj_telefona.data,user_id=current_user.id)
            db.session.add(podaci)
            db.session.commit()
            flash("Uspešno dodavanje podataka!",'success')
            
    return redirect(url_for('.korisnik_page'))


@user_blueprint.route('/korisnik/promena-lozinke',methods=['POST'])
@login_required
def promena_lozinke():
    form_promena = PromenaLozinke(prefix='promena')
    korisnik = User.query.filter_by(id=current_user.id).first()
    
    if form_promena.is_submitted():
        korisnik_hashed_password = korisnik.password
        trenutna_lozinka = form_promena.trenutna_lozinka.data

        if check_password_hash(korisnik_hashed_password,trenutna_lozinka):
            nova_lozinka = form_promena.nova_lozinka.data
            ponovljena_nova_lozinka = form_promena.ponovljena_nova_lozinka.data
            
            if nova_lozinka == ponovljena_nova_lozinka:
                nova_lozinka_hashed = generate_password_hash(nova_lozinka)
                korisnik.password = nova_lozinka_hashed
                db.session.commit()
                flash("Uspešna izmena lozinke!",'success')
            else:
                flash('Nove lozinke se ne poklapaju. Pokušaj ponovno.',category='danger')
        else:
            flash('Trenutne lozinke se ne poklapaju. Pokušaj ponovno.',category='danger')

    return redirect(url_for('.korisnik_page'))
        


@user_blueprint.route('/korisnik/adresa',methods=['POST'])
@login_required
def korisnik_adresa():
    form_podaci = PodaciForm(prefix='podaci')
    korisnik_podaci = Podaci.query.filter_by(user_id=current_user.id).first()    
    if form_podaci.is_submitted():
        if korisnik_podaci is not None:
            korisnik_podaci.adresa = form_podaci.ulica.data
            korisnik_podaci.broj_ulice = form_podaci.kucni_broj.data
            korisnik_podaci.drzava = form_podaci.drzava.data
            korisnik_podaci.grad = form_podaci.grad.data
            korisnik_podaci.postanski_broj = form_podaci.postanski_broj.data
            db.session.commit()
            flash("Uspešno ažuriranje adrese!",'success')
        else:
            podaci = Podaci(adresa=form_podaci.ulica.data,broj_ulice=form_podaci.kucni_broj.data,\
            grad=form_podaci.grad.data,drzava=form_podaci.drzava.data,postanski_broj=form_podaci.postanski_broj.data,user_id=current_user.id)
            db.session.add(podaci)
            db.session.commit()
            flash("Uspešno dodavanje adrese!",'success')
            
    return redirect(url_for('.korisnik_page'))


    