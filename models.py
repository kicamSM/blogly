"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    __tablename__ = 'users'
    
    def __repr__(self):
        u = self
        return f"< User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}"
    
    id = db.Column(db.Integer, 
            
                primary_key=True,
                autoincrement=True)
    
    first_name = db.Column(db.String(20),
                     nullable=False,
                     unique=True)
    
    last_name = db.Column(db.String(20),
                    nullable=False)
    
    image_url = db.Column(db.String)
    # note that there probably is a constraint that you can put on this to make sure it is a url but I havent found it yet.
    