from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            next_url = request.args.get("next")
            # prevent open redirects; only allow internal paths
            if not next_url or not next_url.startswith("/"):
                next_url = url_for("admin.dashboard")
            return redirect(next_url)

        flash("Invalid username or password", "danger")

    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    logout_user()
    flash("Logged out", "success")
    return redirect(url_for("auth.login"))
