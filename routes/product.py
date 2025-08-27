# routes/product.py
from flask import Blueprint, render_template
from models import Product

bp = Blueprint("product", __name__)

@bp.route("/product")
def product():
    # Query DB and convert each row to the FakeStore-like dict your Vue expects
    rows = Product.query.order_by(Product.id.desc()).all()
    products = [
        {
            "id": p.id,
            "title": p.title,
            "price": float(p.price or 0),
            "description": p.description or "",
            "category": p.category or "",
            "image": p.image or "",  # can be full URL or /static/... path
            "rating": {"rate": float(p.rating_rate or 0), "count": int(p.rating_count or 0)},
        }
        for p in rows
    ]
    return render_template("views/product.html", products=products)
