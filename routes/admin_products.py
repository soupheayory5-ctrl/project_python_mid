# routes/admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func, or_
from sqlalchemy.exc import SQLAlchemyError
from models import db, Product
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import redirect, url_for, request
from flask_login import current_user

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.before_request
def require_login_for_admin():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login", next=request.url))
# ---- Dashboard: quick stats -------------------------------------------------
@bp.route("/")
def dashboard():
    total_products = db.session.query(func.count(Product.id)).scalar() or 0
    avg_price = db.session.query(func.avg(Product.price)).scalar()
    category_count = db.session.query(func.count(func.distinct(Product.category))).scalar() or 0
    newest = Product.query.order_by(Product.created_at.desc()).first()
    return render_template(
        "admin/dashboard.html",
        total_products=total_products,
        avg_price=avg_price,
        category_count=category_count,
        newest=newest,
    )

# ---- List & search ----------------------------------------------------------
@bp.route("/products/")
def products_index():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    q = (request.args.get("q") or "").strip()

    query = Product.query
    if q:
        query = query.filter(or_(
            Product.title.ilike(f"%{q}%"),
            Product.category.ilike(f"%{q}%")
        ))

    pagination = query.order_by(Product.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template(
        "admin/products.html",
        products=pagination.items,
        pagination=pagination,
        q=q,
    )

# ---- Create -----------------------------------------------------------------
@bp.route("/products/new", methods=["GET", "POST"])
def products_create():
    if request.method == "POST":
        try:
            p = Product(
                title=(request.form.get("title") or "").strip(),
                price=float(request.form.get("price") or 0),
                description=(request.form.get("description") or "").strip(),
                category=(request.form.get("category") or "").strip(),
                image=(request.form.get("image") or "").strip(),
                rating_rate=float(request.form.get("rating_rate") or 0),
                rating_count=int(request.form.get("rating_count") or 0),
            )
            if not p.title:
                flash("Title is required", "danger")
                return render_template("admin/product_form.html", product=None)
            db.session.add(p)
            db.session.commit()
            flash("Product created", "success")
            return redirect(url_for("admin.products_index"))
        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()
            flash(f"Error creating product: {e}", "danger")
    return render_template("admin/product_form.html", product=None)

# ---- Edit -------------------------------------------------------------------
@bp.route("/products/<int:pid>/edit", methods=["GET", "POST"])
def products_edit(pid: int):
    p = Product.query.get_or_404(pid)
    if request.method == "POST":
        try:
            p.title = (request.form.get("title") or p.title).strip()
            p.price = float(request.form.get("price") or p.price)
            p.description = (request.form.get("description") or p.description).strip()
            p.category = (request.form.get("category") or p.category).strip()
            p.image = (request.form.get("image") or p.image).strip()
            p.rating_rate = float(request.form.get("rating_rate") or p.rating_rate)
            p.rating_count = int(request.form.get("rating_count") or p.rating_count)
            db.session.commit()
            flash("Product updated", "success")
            return redirect(url_for("admin.products_index"))
        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()
            flash(f"Error updating product: {e}", "danger")
    return render_template("admin/product_form.html", product=p)

# ---- Delete -----------------------------------------------------------------
@bp.route("/products/<int:pid>/delete", methods=["POST"])
def products_delete(pid: int):
    p = Product.query.get_or_404(pid)
    try:
        db.session.delete(p)
        db.session.commit()
        flash("Product deleted", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error deleting product: {e}", "danger")
    return redirect(url_for("admin.products_index"))
