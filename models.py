"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.orm import relationship, backref



db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False, unique=True)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String)

    post = db.relationship('Post', cascade="all, delete-orphan")
      
    def __repr__(self):
        u = self
        return f"< user_id={u.user_id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}"

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', backref=backref("posts", cascade="all, delete-orphan"))
    
    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} user_id={p.user_id} created_at={p.created_at}>"
