from flask import Blueprint,jsonify,render_template,session,redirect,request, url_for
from flask_login import login_required,current_user
from models import *
from proizvodi import dobavi_proizvode
from proizvodi import stripe
from forms import PodaciForm
from config import db,send_purchase_email
import stripe

stripe.api_key = "sk_test_51KpDc2HWcPcdTkMNg3fTxBusO5FLBOomptkRp7xzYMp6UY919vJ2oIEVWMC3VLxb3ta0kp0FXYebbn77681y8DOj007ZQrLRc9"

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
    if 'korpa' in session:
        proizvodi = session['korpa']
        ukupna_cena = 0
        for p in proizvodi:
            ukupna_cena += p['price_data']['unit_amount']
        if len(proizvodi) == 0:
            proizvodi = None
    else:
        proizvodi = None
    return render_template("kupovina/checkout.html",proizvodi=proizvodi,ukupna_cena=ukupna_cena)



@views_blueprint.route("/kosarica/placanje",methods=["GET","POST"])
@login_required
def kupovina_podaci():
    if session.get('korpa'):
        form = PodaciForm()
        korisnik_podaci = Podaci.query.filter_by(user_id=current_user.id).first()

        if request.method == "POST" and form.is_submitted():
            if korisnik_podaci is not None:
                korisnik_podaci.ime = form.ime.data
                korisnik_podaci.prezime = form.prezime.data
                korisnik_podaci.broj_telefona = form.broj_telefona.data
                korisnik_podaci.adresa = form.ulica.data
                korisnik_podaci.broj_ulice = form.kucni_broj.data
                korisnik_podaci.drzava = form.drzava.data
                korisnik_podaci.grad = form.grad.data
                korisnik_podaci.postanski_broj = form.postanski_broj.data
                db.session.commit()
                return redirect(url_for('.kupovina'))

            if korisnik_podaci is None:
                podaci = Podaci(ime=form.ime.data,prezime=form.prezime.data,\
                broj_telefona=form.broj_telefona.data,adresa=form.ulica.data,
                broj_ulice=form.kucni_broj.data,grad=form.grad.data,drzava=form.drzava.data,\
                postanski_broj=form.postanski_broj.data,user_id=current_user.id)
                db.session.add(podaci)
                db.session.commit()
                return redirect(url_for('.kupovina'))
            
        else:
            if korisnik_podaci is not None:
                form.ime.data = korisnik_podaci.ime
                form.prezime.data = korisnik_podaci.prezime
                form.broj_telefona.data = korisnik_podaci.broj_telefona
                form.ulica.data = korisnik_podaci.adresa
                form.kucni_broj.data = korisnik_podaci.broj_ulice
                form.grad.data = korisnik_podaci.grad
                form.postanski_broj.data = korisnik_podaci.postanski_broj

            return render_template("kupovina/placanje.html",form=form,korisnik_podaci=korisnik_podaci)
    else:
        return redirect(url_for('.home'))




@views_blueprint.route('/kosarica/kupi', methods=['GET','POST'])
def kupovina():
    load_user = User.query.filter_by(id=current_user.id).first()
    print(load_user.customer_id)
    if load_user.customer_id is None:
        podaci = Podaci.query.filter_by(user_id=current_user.id).first()
        customer = stripe.Customer.create(
            address={
                'city':podaci.grad,
                'line1':podaci.adresa,
                'line2':podaci.broj_ulice,
                'postal_code':podaci.postanski_broj
            },
            name = f'{podaci.ime} {podaci.prezime}',
            phone=podaci.broj_telefona,
            email = current_user.email
        )
        load_user.customer_id = customer['id']
        db.session.commit()

        korpa = session['korpa']
        checkout_session = stripe.checkout.Session.create(
        line_items=korpa,
        payment_method_types=['card'],
        mode='payment',
        customer=customer['id'],
        success_url=request.host_url + 'narudzba/uspesno',
        cancel_url=request.host_url +  'narudzba/neuspesno'
    )
        return redirect(checkout_session.url)
    else:
        podaci_update = Podaci.query.filter_by(user_id=current_user.id).first()
        stripe.Customer.modify(
            current_user.customer_id,
            address={
                'city':podaci_update.grad,
                'line1':podaci_update.adresa,
                'line2':podaci_update.broj_ulice,
                'postal_code':podaci_update.postanski_broj
            },
            name = f'{podaci_update.ime} {podaci_update.prezime}',
            phone=podaci_update.broj_telefona,
            email = current_user.email
        )
        korpa = session['korpa']
        checkout_session = stripe.checkout.Session.create(
        line_items=korpa,
        payment_method_types=['card'],
        mode='payment',
        customer=current_user.customer_id,
        success_url=request.host_url + 'narudzba/uspesno',
        cancel_url=request.host_url +  'narudzba/neuspesno'
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


@views_blueprint.route('/narudzba/uspesno')
def uspesno():
    proizvodi = session['korpa']
    ukupna_cena = 0
    for p in proizvodi:
        ukupna_cena += p['price_data']['unit_amount']
    send_purchase_email(render_template('kupovina/prikaz_narudzbe_email.html',proizvodi=proizvodi,ukupna_cena=ukupna_cena))
    session.pop('korpa',None)
    session.pop('kolicina',None)
    return render_template('kupovina/success.html')


@views_blueprint.route('/narudzba/neuspesno')
def neuspesno():
    return render_template('kupovina/cancel.html')

@views_blueprint.route('/test')
def test():
    proizvodi = session['korpa']
    ukupna_cena = 0
    for p in proizvodi:
        ukupna_cena += p['price_data']['unit_amount']
    return render_template('kupovina/prikaz_narudzbe_email.html',proizvodi=proizvodi,ukupna_cena=ukupna_cena)