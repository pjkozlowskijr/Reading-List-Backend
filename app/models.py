from app import db, login
from flask_login import UserMixin
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, index=True, unique=True)
    token_exp = db.Column(db.DateTime)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    
    def __repr__(self):
        return f"<User: {self.email} | {self.id}"

    def __str__(self):
        return f"<User: {self.email} | {self.first_name} {self.last_name}"

    def hash_pass(self, orig_pass):
        return generate_password_hash(orig_pass)

    def confirm_pass(self, login_pass):
        return check_password_hash(self.password, login_pass)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_on": self.created_on,
            "is_admin": self.is_admin,
            "token": self.token
        }
    
    def from_dict(self, data): 
        for field in ["first_name", "last_name", "email", "password"]:
            if field in data:
                setattr(self, field, data[field])
                if field == "password":
                    self.password = self.hash_pass(data["password"])

    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        if self.token and self.token_exp > current_time + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_exp = dt.utcnow() - timedelta(seconds=61)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if not user or user.token_exp < dt.utcnow():
            return None
        return user

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    subject = db.Column(db.String)
    summary = db.Column(db.Text)
    pages = db.Column(db.Integer)
    image = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return f"<Book: {self.title} | {self.id}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return{
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "subject": self.subject,
            "summary": self.summary,
            "pages": self.pages,
            "image": self.image,
            "created_on": self.created_on
        }

    def from_dict(self, data):
        for field in ["title", "author", "subject", "summary", "pages", "image"]:
            if field in data:
                setattr(self, field, data[field])
