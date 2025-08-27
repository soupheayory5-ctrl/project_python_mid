# routes/home.py
from flask import Blueprint, render_template
from models import Product

bp = Blueprint("home", __name__)

@bp.route("/")
def home():
    # newest 6 products; adjust as you like
    products = (Product.query
                .order_by(Product.created_at.desc())
                .limit(6)
                .all())
    return render_template("views/home.html", products=products)
