from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,TextAreaField,IntegerField,SelectField
from wtforms.validators import InputRequired,Length


class RegisterForm(FlaskForm):
    username = StringField('Korisničko ime',validators=[InputRequired(),Length(max=20)],render_kw={'placeholder':'Unesite korisničko ime','class':'form-control','style':'font-size:13px;'})
    email = EmailField('Email',validators=[InputRequired(),Length(max=50)],render_kw={'placeholder':'Unesite email adresu','class':'form-control','style':'font-size:13px;'})
    password = PasswordField('Lozinka',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Lozinka','class':'form-control','style':'font-size:13px;'})   
    confirm_password = PasswordField('Ponovite lozinku',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Lozinka','class':'form-control','style':'font-size:13px;'}) 

class LoginForm(FlaskForm):
    username = StringField('Korisničko ime',validators=[InputRequired(),Length(max=20)],render_kw={'placeholder':'Korisničko ime','class':'form-control','style':'font-size:13px;'})
    password = PasswordField('Lozinka',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Lozinka','class':'form-control','style':'font-size:13px;'})   

class CenaForm(FlaskForm):
    cena = IntegerField('Cena',validators=[InputRequired()],render_kw={'placeholder':'Cena','class':'form-control','style':'font-size:13px;'})
    valuta = StringField('Valuta',render_kw={'placeholder':'Valuta','class':'form-control','style':'font-size:13px;','value':'HRK','readonly':True})
    product_id = SelectField('Product ID',choices=[],validators=[InputRequired()],render_kw={'class':'form-control','style':'font-size:13px;'})

class ProizvodForm(FlaskForm):
    naziv = StringField('Naziv',validators=[InputRequired(),Length(max=60)],render_kw={'placeholder':'Naziv','class':'form-control','style':'font-size:13px;'})
    opis = TextAreaField('Opis',validators=[InputRequired()],render_kw={'placeholder':'Kratki Opis','class':'form-control','style':'font-size:13px;'})
    img =  StringField('Slika',validators=[InputRequired(),Length(max=300)],render_kw={'placeholder':'Image URL','class':'form-control','style':'font-size:13px;'})
    