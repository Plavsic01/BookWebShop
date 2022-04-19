from flask_login import UserMixin
from config import db,func


class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50),unique=True,nullable=False)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(256),nullable=False)
    avatar = db.Column(db.LargeBinary)
    is_admin = db.Column(db.Boolean,server_default="0")
    date_created = db.Column(db.DateTime(timezone=True),server_default=func.now())
    podaci_usera = db.relationship('Podaci',cascade="all,delete",backref='user')

    def __repr__(self) -> str:
        return f'Username: {self.username}'

class Podaci(db.Model):
    __tablename__ = "adresa"
    id = db.Column(db.Integer,primary_key=True)
    ime = db.Column(db.String(30),nullable=False)
    prezime = db.Column(db.String(30),nullable=False)
    adresa = db.Column(db.String(50),nullable=False)
    broj_ulice = db.Column(db.String(10),nullable=False)
    broj_stana = db.Column(db.Integer,nullable=True)
    grad = db.Column(db.String(50),nullable=False)
    postanski_broj = db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),unique=True)


class Proizvod(db.Model):
    __tablename__ = "proizvod"
    naziv = db.Column(db.String(60),nullable=False)
    opis = db.Column(db.Text,nullable=False)
    # mozda jos dodati duzi opis
    # kad se klikne na knjigu da bude detaljniji opis
    img = db.Column(db.String(300),nullable=False)
    product_id = db.Column(db.String(60),nullable=False,primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True),server_default=func.now())
    cena = db.relationship('Cena',cascade="all,delete",backref='proizvod')
         
    def __repr__(self) -> str:
        return f'Knjiga: {self.naziv}'


class Cena(db.Model):
    __tablename__ = "cena"
    id = db.Column(db.Integer,primary_key=True)
    price_id = db.Column(db.String(60),nullable=True)
    cena_proizvoda = db.Column(db.Integer,nullable=False)
    valuta = db.Column(db.String(3),nullable=False)
    proizvod_id = db.Column(db.String(60),db.ForeignKey('proizvod.product_id'),nullable=False,unique=True) 
    
    def __repr__(self) -> str:
        return f'ID: {self.price_id} Cena: {self.cena_proizvoda} HRK'