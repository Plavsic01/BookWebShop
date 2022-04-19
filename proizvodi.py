import stripe
from config import db
from models import Proizvod,Cena

stripe.api_key = "sk_test_51KpDc2HWcPcdTkMNg3fTxBusO5FLBOomptkRp7xzYMp6UY919vJ2oIEVWMC3VLxb3ta0kp0FXYebbn77681y8DOj007ZQrLRc9"

def kreiraj_cenu(cena:int,currency:str,product_id:str):
    try:
        nova_cena = stripe.Price.create(unit_amount=cena*100,currency=currency,product=product_id)
        dodaj_cenu = Cena(price_id = nova_cena['id'],cena_proizvoda = cena,valuta = nova_cena['currency'],proizvod_id = nova_cena['product'])
        db.session.add(dodaj_cenu)
        db.session.commit()
    except:
        print("Nešto je pošlo po zlu...") # PRIVREMENO REŠENJE...

def dobavi_cenu(price_id):
    try:
        price = stripe.Price.retrieve(price_id)
        return price['product']
    except:
        return False


def kreiraj_proizvod(name:str,description:str,images:list):
    try:
        novi_proizvod = stripe.Product.create(name=name,description=description,images=images)
        dodaj_proizvod = Proizvod(naziv=novi_proizvod['name'],opis=novi_proizvod['description'],img=novi_proizvod['images'][0],product_id=novi_proizvod['id'])
        db.session.add(dodaj_proizvod)
        db.session.commit()
    except:
        print("Nešto je pošlo po zlu...") # PRIVREMENO REŠENJE


def obrisi_proizvod(product_id:str,price_id=None):
    try:
        if price_id is not None:
            if dobavi_cenu(price_id == product_id) == False:
                stripe.Product.delete(product_id)
                return True
        else:
            stripe.Product.delete(product_id)
            return True
    except:
        return False



def dobavi_proizvode(limit=None):
    if limit is not None:
        return stripe.Product.list(limit=limit)

    return stripe.Product.list()

