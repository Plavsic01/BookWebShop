from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,TextAreaField,IntegerField,SelectField
from wtforms.validators import InputRequired,Length,NumberRange


class RegisterForm(FlaskForm):
    username = StringField('Korisničko ime',validators=[InputRequired(),Length(max=20)],render_kw={'placeholder':'Unesite korisničko ime','class':'form-control','style':'font-size:13px;'})
    email = EmailField('Email',validators=[InputRequired(),Length(max=50)],render_kw={'placeholder':'Unesite email adresu','class':'form-control','style':'font-size:13px;'})
    password = PasswordField('Lozinka',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Lozinka','class':'form-control','style':'font-size:13px;'})   
    confirm_password = PasswordField('Ponovite lozinku',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Lozinka','class':'form-control','style':'font-size:13px;'}) 

class LoginForm(FlaskForm):
    username = StringField('Korisničko ime',validators=[InputRequired(),Length(max=20)],render_kw={'placeholder':'Korisničko ime','class':'form-control','style':'font-size:13px;'})
    password = PasswordField('Lozinka',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Lozinka','class':'form-control','style':'font-size:13px;'})   

    
class ProizvodForm(FlaskForm):
    naziv = StringField('Naziv',validators=[InputRequired(),Length(max=60)],render_kw={'placeholder':'Naziv','class':'form-control','style':'font-size:13px;'})
    opis = TextAreaField('Opis',validators=[InputRequired()],render_kw={'placeholder':'Kratki Opis','class':'form-control','style':'font-size:13px;'})
    img =  StringField('Slika',validators=[InputRequired(),Length(max=300)],render_kw={'placeholder':'Image URL','class':'form-control','style':'font-size:13px;'})
    cena = IntegerField('Cena',validators=[InputRequired()],render_kw={'placeholder':'Cena','class':'form-control','style':'font-size:13px;'})
    valuta = StringField('Valuta',render_kw={'placeholder':'Valuta','class':'form-control','style':'font-size:13px;','value':'HRK','readonly':True})
    dostupna_kolicina = IntegerField('Dostupna količina',validators=[InputRequired()],render_kw={'placeholder':'Dostupna Količina','class':'form-control','style':'font-size:13px;'})

class PodaciForm(FlaskForm):
    ime = StringField('Ime*',validators=[InputRequired(),Length(max=60)],render_kw={'placeholder':'Ime (obavezno)','class':'form-control','style':'font-size:13px;'})
    prezime = StringField('Prezime*',validators=[InputRequired(),Length(max=60)],render_kw={'placeholder':'Prezime (obavezno)','class':'form-control','style':'font-size:13px;'})
    email = EmailField('E-mail*',validators=[InputRequired(),Length(max=60)],render_kw={'placeholder':'Email adresa (obavezno)','class':'form-control','style':'font-size:13px;'})
    broj_telefona = StringField('Broj telefona*',validators=[InputRequired(),Length(max=10)],render_kw={'placeholder':'Broj telefona (obavezno)','class':'form-control','style':'font-size:13px;'})
    drzava = SelectField('Država*',choices=['Hrvatska'],render_kw={'readonly':True,'class':'form-control form-control-rounded'})
    ulica = StringField('Ulica*',validators=[InputRequired(),Length(max=60)],render_kw={'placeholder':'Naziv ulice (obavezno)','class':'form-control','style':'font-size:13px;'})
    kucni_broj = StringField('Kućni broj*',validators=[InputRequired(),Length(max=60)],render_kw={'placeholder':'Kućni broj (obavezno)','class':'form-control','style':'font-size:13px;'})
    grad = StringField('Grad*',validators=[InputRequired(),Length(max=60)],render_kw={'placeholder':'Grad (obavezno)','class':'form-control','style':'font-size:13px;'})
    postanski_broj = StringField('Poštanski broj*',validators=[InputRequired(),Length(max=60)],render_kw={'placeholder':'Poštanski broj (obavezno)','class':'form-control','style':'font-size:13px;'})



class PromenaLozinke(FlaskForm):
    trenutna_lozinka = PasswordField('Trenutna lozinka',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Trenutka lozinka','class':'form-control','style':'font-size:13px;'})   
    nova_lozinka = PasswordField('Nova lozinka',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Nova lozinka','class':'form-control','style':'font-size:13px;'})   
    ponovljena_nova_lozinka = PasswordField('Ponovite novu lozinku',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Ponovljena nova lozinka','class':'form-control','style':'font-size:13px;'})   