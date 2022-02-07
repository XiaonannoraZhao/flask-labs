from flask_app import db 
from flask_app.models import User,Post, Comment

db.drop_all()
db.create_all()

#user1 = User(username="user1",email="user1@test.ac.uk", password="passuser1")
#user2 =User(username="user2@test.ac.uk",email="user2@test.ac.uk",password="passuser2")
#user3 = User(username="user3@test.ac.uk",email="user3@test.ac.uk", password="passuser3")#

#post1=Post(title="post 1",
#content="contentc1",author_id=1)
#post2=Post(title="post 2",
#content="contentc2",author_id=2)
#post3=Post(title="post 3",
#content="contentc3",author_id=3)#
#

##comment= Comment(comment="This is my comment",user=user1,post=post1)
##db.session.add_all([user1,user2,user3])
#db.session.add_all([post1,post2,post3])
#db.session.commit()