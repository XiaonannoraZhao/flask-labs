from datetime import datetime
import email
from operator import and_
from flask_app import db, login_manager
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_
# one


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(40), nullable=False,
                           default='default.jpg')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.date}', '{self.title}', '{self.content}')"
# one


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128))
    post = db.relationship('Post', backref='user', lazy=True)
    comment = db.relationship('Comment', backref='user', lazy=True)
  

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

# many


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    @classmethod
    def getCommentsByPost(cls, post_id):
        commentList = cls.query.filter(cls.post_id == post_id).all()
        print("++++++++", commentList)
        returnObjects = []
        for comment in commentList:
            user = User.query.get_or_404(comment.user_id)
            obj = {
                'id': comment.id,
                'comment': comment.comment,
                'user': user,
                'post_id': comment.post_id,
            }
            returnObjects.append(obj)
        print(returnObjects)
        return returnObjects


class Rating(db.Model):
    """Rating in ratings database"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer,  nullable=False)
    score = db.Column(db.Integer, nullable=False)

    @classmethod
    def addOrUpdate(cls, post_id, rateNum):
        rateObj = Rating.query.filter(and_(
            cls.post_id == post_id,cls.user_id == current_user.id)).first()
        if rateObj is None:
            rateObject = Rating(
                post_id=post_id,
                user_id=current_user.id,
                score=rateNum
            )
            db.session.add(rateObject)
            db.session.commit()
            return rateObject            
        else:
            rateObj.score = rateNum
            db.session.commit()
            return rateObj

    @classmethod
    def getCurrentUserRate(cls, _id):
        if len(vars(current_user)) != 0:
            rateObj = cls.query.filter(and_(cls.post_id == _id, cls.user_id == current_user.id)).first()
            if rateObj is None:
                return 0
            else:
                return rateObj.score
        else:
            return 0

    
# adated from Grinberg(2014, 2018)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
