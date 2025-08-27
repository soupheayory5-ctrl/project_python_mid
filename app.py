import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from models import db, User
from routes import register_blueprints
from mail_config import mail  # mail = Mail() in mail_config.py

load_dotenv()

login_manager = LoginManager()

def _boolenv(name: str, default: bool) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return str(v).lower() in ("1", "true", "yes", "on")

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # --- Core config ---
    db_path = os.path.join(app.root_path, "store.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # app.py (inside create_app)
    # app.py (only the DB URI part shown)
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        # Render sometimes gives postgres://, SQLAlchemy wants postgresql://
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    else:
        db_path = os.path.join(app.root_path, "store.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    # --- Mail (from .env) ---
    mail_username = os.getenv("MAIL_USERNAME")
    app.config.update(
        MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
        MAIL_USE_TLS=_boolenv("MAIL_USE_TLS", True),
        MAIL_USE_SSL=_boolenv("MAIL_USE_SSL", False),
        MAIL_USERNAME=mail_username,
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        # fallback to username if MAIL_DEFAULT_SENDER not provided
        MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER", mail_username),
    )

    # init extensions
    db.init_app(app)
    Migrate(app, db)
    mail.init_app(app)  # ← IMPORTANT

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # blueprints
    register_blueprints(app)
    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
