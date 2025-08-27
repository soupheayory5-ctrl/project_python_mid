from flask import Blueprint, render_template
bp = Blueprint("checkout", __name__)

@bp.route("/checkout")
def checkout():
    return render_template("views/checkout.html")
