from flask_sqlalchemy import SQLAlchemy
from requests import session
from sqlalchemy.sql import func
from flask_mail import Mail,Message

db = SQLAlchemy()
mail = Mail()


def send_registration_mail():
    msg = Message(subject="USPESNA REGISTRACIJA",
                  sender='lessonsprogramming@gmail.com',
                  recipients=["andrejplavsic3@gmail.com"])
    try:
        mail.send(msg)
    except:
        print("doslo je do greske")


def send_purchase_email(template):
    msg = Message(subject="Hvala Na Narudzbi!",
                  sender='lessonsprogramming@gmail.com',
                  recipients=["andrejplavsic3@gmail.com"])
    msg.html = template
    try:
        mail.send(msg)
    except:
        print("doslo je do greske")