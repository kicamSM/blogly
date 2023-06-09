"""Seed file to make sample data for db"""

from models import User, Post, Tag, PostTag, db 
from app import app

# create all tables 
db.drop_all()
db.create_all()

# PostTag.query.delete()
# User.query.delete()
# Post.query.delete()
# Tag.query.delete()


abe = User(user_id='1',first_name="Abe", last_name="Lincoln", image_url="http://placekitten.com/g/200/300")
george = User(user_id='2',first_name="George", last_name="Washington", image_url="http://placekitten.com/g/300/300")
samuel = User(user_id='3',first_name="Samuel", last_name="Adams", image_url="http://placekitten.com/g/400/400")
donald = User(user_id='4',first_name="Donald", last_name="Trump", image_url="http://placekitten.com/g/500/500")

p1 = Post(title="On Slavery", content="Four score and seven years ago....", user_id='1')
p2 = Post(title="On the Civil War", content="our forefathers....", user_id='1')
p3 = Post(title="Untimely Tweets", content="This is an important notification sent out via Tweet", user_id='4')
p4 = Post(title="The Adams Family", content="Presidents Run in our Family", user_id='3')
p5 = Post(title="The first is the best", content="Declaration of Independence", user_id='2')

db.session.add_all([abe, george, samuel, donald, p1, p2, p3, p4, p5])

db.session.commit()

# ta = Tag(name='history', post_with_tag=[PostTag(post_id=p1.id)])

# tb = Tag(name='firsts', post_with_tag=[PostTag(post_id=p3.id)])
# do you need a tag id in there???? will it be automated???
t1 = Tag(name="history")
t2 = Tag(name="firsts")

db.session.add_all([t1, t2])
db.session.commit()

# Note that an error you are getting when trying to add to the list a new user. That the id is taken because you set some ids so you have to try and add until you get to 5 because the user_id is taken from 1-4. There should be a way to fix this. Should not be an issue when actually running the app if you are not pre-loading people into it. 