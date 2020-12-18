from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime


class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50))
    password=db.Column(db.Text)
    data=db.relationship('Data',backref='author')
    

    def set_password(self,password):
        self.password=generate_password_hash(password)
        return self.password
    
    def get_password(self,password):
        return check_password_hash(self.password,password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Data(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    amount_income=db.Column(db.Integer)
    amount_spent=db.Column(db.Integer)
    total=db.Column(db.Integer)
    users_id=db.Column(db.Integer,db.ForeignKey('users.id'))

  

