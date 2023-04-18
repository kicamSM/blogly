"""Blogly application."""
import warnings
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()

app.config['SECRET_KEY'] = "iloverollerderby12"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
# db.create_all()

try:
    from flask_debugtoolbar import DebugToolbarExtension
    debug = DebugToolbarExtension(app)
except ImportError:
    warnings.warn('Debugging disabled. Install flask_debugtoolbar to enable')
    pass

@app.route('/')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('list.html', users=users)

# render_template('list.html', users=users)
# "hello world"

@app.route('/', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(f"/{new_user.id}")


@app.route('/<int:user_id>')
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

# @app.route('/add', methods=["POST"])
# def create_user():
#     """edit details about a single user"""
#     first_name = request.form["first_name"]
#     last_name = request.form["last_name"]
#     image_url = request.form["image_url"]
    
#     new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
#     db.session.add(new_user)
#     db.session.commit()
    
#     return redirect(f"/{new_user.id}")
    

@app.route('/edit/<int:user_id>')
# <int:user_id>
def edit_user(user_id):
    """edit details about a single user"""
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)

@app.route('/edit<int:user_id>', methods=["POST"])
def post_edited_user(user_id):
    user = User.query.get(user_id)
    # session.delete(user)
    # db.session.commit()
    
    user.name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    user.user_id = user_id
    
    # user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/{user.id}")
    
@app.route('/<int:user_id>/delete', methods=["POST"])
# <int:user_id>
def delete_user(user_id):
    """edit details about a single user"""
    user = User.query.get(user_id).delete()
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/')