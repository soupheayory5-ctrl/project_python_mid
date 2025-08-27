# routes/cart.py
from flask import Blueprint, render_template, request, jsonify
from models import Product

bp = Blueprint("cart", __name__)

@bp.route("/cart")
def cart():
    # just render the template; data is fetched via JS
    return render_template("views/cart.html")

@bp.route("/api/products/by_ids", methods=["POST"])
def products_by_ids():
    """
    Body: {"ids": [1,2,3]}
    Returns: { "1": {...product...}, "2": {...}, ... }  # map by id for easy lookup
    """
    payload = request.get_json(silent=True) or {}
    ids = payload.get("ids") or []
    if not isinstance(ids, list) or not ids:
        return jsonify({})

    rows = (
        Product.query
        .filter(Product.id.in_(ids))
        .all()
    )

    data = {
        p.id: {
            "id": p.id,
            "title": p.title or "",
            "price": float(p.price or 0),
            "description": p.description or "",
            "category": p.category or "",
            "image": p.image or "",
            "rating": {"rate": float(p.rating_rate or 0), "count": int(p.rating_count or 0)},
        }
        for p in rows
    }
    return jsonify(data)
