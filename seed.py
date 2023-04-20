"""Seed file to make sample data for db"""

from models import User, Post, db 
from app import app

# create all tables 
db.drop_all()
db.create_all()

abe = User(user_id='1',first_name="Abe", last_name="Lincoln", image_url="http://placekitten.com/g/200/300")
george = User(user_id='2',first_name="George", last_name="Washington", image_url="http://placekitten.com/g/300/300")
samuel = User(user_id='3',first_name="Samuel", last_name="Adams", image_url="http://placekitten.com/g/400/400")
donald = User(user_id='4',first_name="Donald", last_name="Trump", image_url="http://placekitten.com/g/500/500")

p1 = Post(title="On Slavery", content="Four score and seven years ago....", user_id='1')
p2 = Post(title="On the Civil War", content="our forefathers....", user_id='1')
p3 = Post(title="Untimely Tweets", content="This is an important notification sent out via Tweet", user_id='4')
p4 = Post(title="The Adams Family", content="Presidents Run in our Family", user_id='3')
p5 = Post(title="The first is the best", content="Declaration of Independence", user_id='2')

# p1 = Post(title="On Slavery", content="Four score and seven years ago....", created_at="10/10/1830 @1345")
# p2 = Post(title="On the Civil War", content="our forefathers....", created_at="10/10/1830 @1345")
# p3 = Post(title="Untimely Tweets", content="This is an important notification sent out via Tweet", created_at="10/10/1830 @1345")
# p4 = Post(title="The Adams Family", content="Presidents Run in our Family", created_at="10/10/1830 @1345")
# p5 = Post(title="The first is the best", content="Declaration of Independence", created_at="10/10/1830 @1345")

db.session.add(abe)
db.session.add(george)
db.session.add(samuel)
db.session.add(donald)

db.session.commit()

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)

db.session.commit()

