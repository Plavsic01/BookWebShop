from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField
from wtforms.validators import InputRequired,Length


class RegisterForm(FlaskForm):
    username = StringField('Korisničko ime',validators=[InputRequired(),Length(max=20)],render_kw={'placeholder':'Unesite korisničko ime','class':'form-control','style':'font-size:13px;'})
    email = EmailField('Email',validators=[InputRequired(),Length(max=50)],render_kw={'placeholder':'Unesite email adresu','class':'form-control','style':'font-size:13px;'})
    password = PasswordField('Lozinka',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Lozinka','class':'form-control','style':'font-size:13px;'})   
    confirm_password = PasswordField('Ponovite lozinku',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Lozinka','class':'form-control','style':'font-size:13px;'}) 


class LoginForm(FlaskForm):
    username = StringField('Korisničko ime',validators=[InputRequired(),Length(max=20)],render_kw={'placeholder':'Korisničko ime','class':'form-control','style':'font-size:13px;'})
    password = PasswordField('Lozinka',validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':'Lozinka','class':'form-control','style':'font-size:13px;'})   