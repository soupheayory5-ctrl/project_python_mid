from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()

class Product(db.Model):
    """
    Mirrors fakestoreapi.com/products (flatten 'rating' to 2 columns).
    rating = {"rate": float, "count": int}
    """
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)          # same as fakestore id
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text, nullable=False, default="")
    category = db.Column(db.String(80))
    image = db.Column(db.String(255))                     # URL or /static path
    rating_rate = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # handy helper if you ever want the exact fakestore-like dict
    def store_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            "category": self.category,
            "image": self.image,
            "rating": {"rate": self.rating_rate, "count": self.rating_count},
        }
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="admin")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)