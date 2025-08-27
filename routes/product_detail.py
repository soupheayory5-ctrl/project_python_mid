# routes/product_detail.py
from flask import Blueprint, render_template
from models import Product

bp = Blueprint("product_detail", __name__)

@bp.route("/product_detail/<int:product_id>")
def product_detail(product_id):
    p = Product.query.get_or_404(product_id)
    product = {
        "id": p.id,
        "title": p.title,
        "price": float(p.price or 0),
        "description": p.description or "",
        "category": p.category or "",
        "image": p.image or "",
        "rating": {"rate": float(p.rating_rate or 0), "count": int(p.rating_count or 0)},
    }
    return render_template("views/product_detail.html", product=product)
