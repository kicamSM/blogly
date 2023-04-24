"""Blogly application."""
import warnings
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

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

@app.route('/users')
def list_users_links():
    """Shows list of all users in db with link"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/add')
def display_add_user():
    """Shows add user form"""
    return render_template('add.html')

@app.route('/add', methods=["POST"])
def create_user():
    """creates new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = user.posts
    # user_posts = post.users
    # post = User.query.get_or_404(user_id.id)
    return render_template('details.html', user=user, posts=posts)

@app.route('/<int:user_id>/edit')
def edit_user(user_id):
    """edit details about a single user"""
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)

@app.route('/<int:user_id>/edit', methods=["POST"])
def post_edited_user(user_id):
    """takes the information from form and adds new user"""
    user = User.query.get(user_id)
    
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    
    return redirect("/users")
 
@app.route('/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """edit details about a single user"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_posts_form(user_id):
    """display posts form"""
    # here you need to get all of the tags probably using the User and then render them in the template with a choice to add them to the post -using a checkmark or something 
    user = User.query.get(user_id)
    # post = User.Post.
    tags = Tag.query.all()
    return render_template('new_posts.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_new_post(user_id):
    """display new post"""
    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]
    # checked_tags = request.form.getlist('tags')
    # you are going to have to look this further tomorrow... time for bed.You are getting the data from the checkboxes but then you need to add that information to the tags which I am uncertain how to do at this point. 
    tags_ids = [int(num) for num in request.form.getlist("tags")]
    # this you looked at from answer. What I believe is happening here. We are taking each value which is the tag_id a number(thus calling it num turning it into an integer, and then iterating through each of them. ])
    tags = Tag.query.filter(Tag.id.in_(tags_ids)).all()
    # Then we are taking the from the Tags model, querying and filtering by the tags_ids and obtaining each tag. 
    user_id = user_id
    
    # tc = Tag(name='history', post_with_tag=[PostTag(post_id=p1.id)])
    
    
    new_post = Post(title=title, content=content, user_id=user_id, user=user, tags=tags) 
    # here we did this before we just needed to add the tags to the post so that when we go to post page they are connected to that page. 
    db.session.add(new_post)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/post/<int:post_id>')
def display_post(post_id, user_id):
    """display single post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get(user_id)
    tags = post.tags
    # posts = tag.posts
    # tags = Tag.query.all()
    
    return render_template('post.html', post=post, user=user, tags=tags)

@app.route('/post/<int:post_id>/edit')
def edit_post(post_id):
    """edit details about a single post"""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/edit', methods=["POST"])
def post_edited_post(post_id):
    """takes the information from form and adds the edited post"""
    post = Post.query.get_or_404(post_id)
    
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()
    
    return redirect("/users")

 
@app.route('/post/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """delete post"""
    
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    
    return redirect('/users')

@app.route('/tags')
def list_tags():
    """Lists all tags, with links to the tag detail page"""
    tags = Tag.query.all()
    
    return render_template('tag.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def list_tag_details(tag_id):
    """Lists tag details"""
    tag = Tag.query.get_or_404(tag_id)
    # posts = Post.query.get_or_404(tag_id)
    # posts = tag.post_with_tag 
    posts = tag.posts
    
    return render_template('tag_details.html', tag=tag, posts=posts)

@app.route('/tags/new')
def display_new_tag_form():
    """Displays new tag form"""
    return render_template('add_tag.html')

@app.route('/tags/new', methods=['POST'])
def create_tag():
    """Creates a new tag"""
    name = request.form["name"]
    
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Displays edit form for tags"""
    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def posts_edited_tag(tag_id):
    """Posts edited changes"""
    tag = Tag.query.get(tag_id)
    
    tag.name = request.form["name"]
    db.session.add(tag)
    db.session.commit()
    
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Deletes Tag"""
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    
    return redirect('/tags')


