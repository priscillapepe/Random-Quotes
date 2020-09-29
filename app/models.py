
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from . import db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index =True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(5000))
    profile_pic_path = db.Column(db.String)
    pass_secure = db.Column(db.String(255))
    date_joined = db.Column(db.DateTime,default=datetime.utcnow)

    quote = db.relationship('Quote',backref = 'user',lazy = "dynamic")

    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'



class Quote(db.Model):
    __tablename__ = 'quote'

    id = db.Column(db.Integer,primary_key = True)
    quote_title = db.Column(db.String)
    quote_content = db.Column(db.String(1000))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
   
    comments = db.relationship('Comment',backref =  'quote_id',lazy = "dynamic")

    def save_quote(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_quote(cls,id):
        quote = Quote.query.filter_by(id=id).first()

        return quote

    @classmethod
    def count_quote(cls,uname):
        user = User.query.filter_by(username=uname).first()
        quote = quote.query.filter_by(user_id=user.id).all()

        quote_count = 0
        for quote in quote:
            quote_count += 1

        return _count

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    quote = db.Column(db.Integer,db.ForeignKey("quote.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,quote):
        comments = Comment.query.filter_by(quote_id=quote).all()
        return comments
    # @classmethod
    # def delete_comment()

