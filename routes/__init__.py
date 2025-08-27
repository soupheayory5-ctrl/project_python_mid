# routes/__init__.py
def register_blueprints(app):
    # Auth FIRST
    from .auth import bp as auth_bp

    # Site pages
    from .home import bp as home_bp
    from .product import bp as product_bp
    from .product_detail import bp as product_detail_bp
    from .about import bp as about_bp
    from .contact import bp as contact_bp
    from .cart import bp as cart_bp
    from .checkout import bp as checkout_bp

    # Misc
    from .telegram_message import bp as telegram_message_bp
    from .send_email import bp as send_email_bp
    from .confirm_khqr import bp as confirm_khqr_bp

    # Admin (single blueprint)
    from .admin import bp as admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(product_detail_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(telegram_message_bp)
    app.register_blueprint(send_email_bp)
    app.register_blueprint(confirm_khqr_bp)
    app.register_blueprint(admin_bp)
