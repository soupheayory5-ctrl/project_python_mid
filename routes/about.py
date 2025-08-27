from flask import Blueprint, render_template
bp = Blueprint("about", __name__)

@bp.route("/about")
def aboutUs():
    return render_template("views/aboutus.html")
