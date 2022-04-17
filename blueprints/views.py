from flask import Blueprint, redirect, render_template, url_for
from models import Proizvod
from config import db
import proizvodi as p

views_blueprint = Blueprint("views_blueprint",__name__)


@views_blueprint.route("/")
def home():
    products = p.dobavi_proizvode()
    return render_template('index.html',products = products)


@views_blueprint.route("/kreiraj")
def kreiraj():
    try:
        novi_proizvod = p.kreiraj_proizvod('Harry Potter','knjiga o carobnjacima, ludacki je dobro, super knjiga',['https://images-na.ssl-images-amazon.com/images/I/91ocU8970hL.jpg'])
        dodaj_proizvod = Proizvod(naziv=novi_proizvod['name'],opis=novi_proizvod['description'],img=novi_proizvod['images'][0],product_id=novi_proizvod['id'],price_id='ovo mi fali')
        db.session.add(dodaj_proizvod)
        db.session.commit()
        return redirect(url_for('views_blueprint.home'))    
    except:
        print("Nešto je pošlo po zlu...") # OVO JE SAMO TRENUTNO RESENJE
    return redirect(url_for('views_blueprint.home'))
