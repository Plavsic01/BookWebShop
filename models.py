from flask_login import UserMixin
from config import db,func
from sqlalchemy.sql import expression

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50),unique=True,nullable=False)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(256),nullable=False)
    customer_id = db.Column(db.String(256),nullable=True)
    is_admin = db.Column(db.Boolean,server_default=expression.false(),nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),server_default=func.now())
    podaci_usera = db.relationship('Podaci',cascade="all,delete",backref='user')

    def __repr__(self) -> str:
        return f'Username: {self.username}'

class Podaci(db.Model):
    __tablename__ = "adresa"
    id = db.Column(db.Integer,primary_key=True)
    ime = db.Column(db.String(30),nullable=True)
    prezime = db.Column(db.String(30),nullable=True)
    broj_telefona = db.Column(db.String(10),nullable=True)
    adresa = db.Column(db.String(50),nullable=True)
    broj_ulice = db.Column(db.String(10),nullable=True)
    grad = db.Column(db.String(50),nullable=True)
    drzava = db.Column(db.String(20),nullable=True)
    postanski_broj = db.Column(db.Integer,nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),unique=True)


# narudzba = db.Table('narudzba',
#     db.Column('user_id',db.Integer,db.ForeignKey('user.id'),primary_key=True),
#     db.Column('proizvod_id',db.Integer,db.ForeignKey('proizvod.id'),primary_key=True),
#     db.Column('status',db.Boolean,server_default=expression.false(),nullable=False),
#     db.Column('datum',db.DateTime(timezone=True),server_default=func.now()),
#     db.Column('kolicina',db.Integer,nullable=False)
# )


class Proizvod(db.Model):
    __tablename__ = "proizvod"
    id = db.Column(db.Integer,primary_key=True)
    naziv = db.Column(db.String(60),nullable=False,unique=True)
    opis = db.Column(db.Text,nullable=False)
    cena_proizvoda = db.Column(db.Integer,nullable=False)
    valuta = db.Column(db.String(3),nullable=False)
    duzi_opis = db.Column(db.Text,nullable=True)
    dostupna_kolicina = db.Column(db.Integer,nullable=False)
    img = db.Column(db.String(300),nullable=False)
    obrisan = db.Column(db.Boolean,server_default=expression.false(),nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),server_default=func.now())

    # podaci = db.relationship('User',secondary=narudzba,backref='proizvodi',cascade="all,delete")

         
    def __repr__(self) -> str:
        return f'Knjiga: {self.naziv}'



