from flask import Blueprint,render_template,redirect,url_for
import proizvodi as p

views_blueprint = Blueprint("views_blueprint",__name__)


@views_blueprint.route("/")
def home():
    products = p.dobavi_proizvode()
    return render_template('index.html',products = products)




