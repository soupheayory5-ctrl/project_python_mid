from flask import Blueprint, render_template
bp = Blueprint("contact", __name__)

@bp.route("/contact")
def contact():
    return render_template("views/contact.html")
