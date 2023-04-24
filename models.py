"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.orm import relationship, backref



db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# Users are like departments each user can have many posts but each post only has one user   
class User(db.Model):
    """User Model"""
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False, unique=True)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String)

    posts = db.relationship('Post', backref="user", cascade="all, delete-orphan")
    # added part into this from solution 
    #backref to users and changed from post to posts
      
    def __repr__(self):
        u = self
        return f"< user_id={u.user_id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}"

# Post is like Employee each post has one user just like each Employee has one department
class Post(db.Model):
    """Post Model"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # user = db.relationship('User', backref=backref("posts", cascade="all, delete-orphan"))
    #so aparrently dont need this. This you followed from the doccumentation direcetly btw
    
    #  user and posts are connected 
    
    # post_with_tag = db.relationship('PostTag', backref='post' )
    # Post is connected to PostTag Not cause of error
    
    tags = db.relationship('Tag', secondary="post_tag", backref="posts")
    # posts and tags are connected NOT CAUSE OF ERROR
    # note that this connects to both tags and post_tag so you dont need anything additional. 
    
    
    
    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} user_id={p.user_id} created_at={p.created_at}>"

    
class PostTag(db.Model):
    """Post Tag Model"""
    __tablename__ = "post_tag"
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    
    # user = db.relationship('Tag', backref=backref("post_tag", cascade="all, delete-orphan"))
    # tried this still wont delete
    
# Tags is like projects we are connecting Tags and Posts just like projects and employees are connected
class Tag(db.Model):
    """Tag Model"""
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True)
    # autoincrement=True this you took this out of tags - not sure if this is correct
    name = db.Column(db.Text, nullable=False, unique=True)
    
    # post_with_tag = db.relationship('PostTag', backref='tag' )
    # # Tag is connected to PostTag
    # post = db.relationship('PostTag', cascade="all, delete-orphan")
    # tried this still wont delete
    # posts = db.relationship('Post', secondary='post_tag',cascade="all,delete", backref='tags')
    # this you looked at the solution for
    
    def __repr__(self):
        p = self
        return f"<Tag_id={p.id} tag_name={p.name}>"