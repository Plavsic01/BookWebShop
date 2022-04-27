from flask import Blueprint,jsonify,render_template,session,redirect,request, url_for
from flask_login import login_required,current_user
from models import *
from proizvodi import dobavi_proizvode
from proizvodi import stripe
from forms import PodaciForm
from config import db

views_blueprint = Blueprint("views_blueprint",__name__)


@views_blueprint.route("/")
def home():
    proizvodi = dobavi_proizvode()
    return render_template('index.html',proizvodi=proizvodi)


@views_blueprint.route("/dodaj-u-korpu/<int:prod_id>",methods=["POST"])
def dodaj_u_korpu(prod_id):
    postoji = False
    if 'kolicina' not in session:
        num = 0
    else:
        num = session['kolicina']['kolicina']

    proizvod = Proizvod.query.filter_by(id=prod_id).first()

    if 'korpa' in session:
        for korpa in session['korpa']:
            if korpa['price_data']['product_data']['name'] == proizvod.naziv:                
                postoji = True

        if postoji == False:
            session['korpa'].append({
            'price_data':{
                'product_data': {
                    'name':proizvod.naziv,
                    'images':[proizvod.img],
                },
                'unit_amount':proizvod.cena_proizvoda,
                'currency':proizvod.valuta,
            },
            'quantity': 1,
        })
            session['kolicina'].update({'kolicina':num+1})
            session.modified = True
    
    else:
        session['korpa'] = [{
        'price_data':{
            'product_data': {
                'name':proizvod.naziv,
                'images':[proizvod.img],
            },
            'unit_amount':proizvod.cena_proizvoda,
            'currency':proizvod.valuta,
        },
        'quantity': 1,      
    }]
        session['kolicina'] = {'kolicina':num+1}
    return jsonify(session['kolicina'])
    


@views_blueprint.route("/kosarica")
def kosarica():
    user = User.query.filter_by(id=current_user.id).first()
    proizvod = Proizvod.query.filter_by(id=1).first()
    narudzba = ProizvodNarudzba(kolicina=1,proizvod_id=proizvod.id)
    narudzba.proizvod.append(user)
    db.session.commit()

    if 'korpa' in session:
        proizvodi = session['korpa']
        if len(proizvodi) == 0:
            proizvodi = None
    else:
        proizvodi = None
    return render_template("kupovina/checkout.html",proizvodi=proizvodi)



@views_blueprint.route("/kosarica/placanje",methods=["GET","POST"])
@login_required
def kupovina_podaci():
    if session.get('korpa'):
        form = PodaciForm()
        korisnik_podaci = Podaci.query.filter_by(user_id=current_user.id).first()
        if korisnik_podaci is not None:
            form.ime.data = korisnik_podaci.ime
            form.prezime.data = korisnik_podaci.prezime
            form.broj_telefona.data = korisnik_podaci.broj_telefona
            form.ulica.data = korisnik_podaci.adresa
            form.kucni_broj.data = korisnik_podaci.broj_ulice
            form.grad.data = korisnik_podaci.grad
            form.postanski_broj.data = korisnik_podaci.postanski_broj

        
        if request.method == "POST" and form.is_submitted():
            if korisnik_podaci is None:
                podaci = Podaci(ime=form.ime.data,prezime=form.prezime.data,\
                broj_telefona=form.broj_telefona.data,adresa=form.ulica.data,
                broj_ulice=form.kucni_broj.data,grad=form.grad.data,drzava=form.drzava.data,\
                postanski_broj=form.postanski_broj.data,user_id=current_user.id)
                db.session.add(podaci)
                db.session.commit()
                return redirect(url_for('.kupovina'))

            return redirect(url_for('.kupovina'))
            
        return render_template("kupovina/placanje.html",form=form)
    else:
        return redirect(url_for('.home'))



@views_blueprint.route('/kosarica/kupi', methods=['GET','POST'])
def kupovina():
    korpa = session['korpa']
    checkout_session = stripe.checkout.Session.create(
        line_items=korpa,
        payment_method_types=['card'],
        mode='payment',
        success_url=request.host_url + '/narudzba/uspesno',
        cancel_url=request.host_url +  '/narudzba/neuspesno'
    )
    return redirect(checkout_session.url)


@views_blueprint.route('/ocisti-kosaricu',methods=['POST'])
def ocisti_kosaricu():
    session.pop('korpa',None)
    session['kolicina'].update({'kolicina':0})
    return jsonify(session['kolicina'])


@views_blueprint.route('/ocisti-kosaricu/<string:prod_naziv>',methods=['POST'])
def ocisti_pojedinacni_proizvod(prod_naziv):
    index_to_delete = None

    for i in range(len(session['korpa'])):
        if session['korpa'][i]['price_data']['product_data']['name'] == prod_naziv:
            index_to_delete = i
            break
    
    session['korpa'].pop(index_to_delete)
    
    kolicina_u_korpi = session['kolicina']['kolicina'] #broj koliko ih je u korpi
    update_kolicina = {'kolicina':kolicina_u_korpi-1}
    session['kolicina'].update(update_kolicina)
    session.modified = True
    
    return jsonify(session['kolicina'])


@views_blueprint.route('/narudzdba/uspesno')
def uspesno():
    for sess in session['korpa']:
        print(sess)
        #dodati u tabelu
    return render_template('kupovina/success.html')


@views_blueprint.route('/narudzdba/neuspesno')
def neuspesno():
    return render_template('kupovina/cancel.html')

