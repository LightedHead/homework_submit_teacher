from datetime import datetime
from app import db
#密码的加密
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from app import login

from hashlib import md5

#管理员信息（教师）
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<用户名:{}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#作业提交情况
class Submit(db.Model):
    __tablename__ = 'submit'
    id = db.Column(db.String(45),primary_key=True)
    #提交者姓名
    student_name = db.Column(db.String(45))
    #提交时间
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    #作业文件名
    filename = db.Column(db.String(128))
    #作业科目
    subject = db.Column(db.String(128))
    def __repr__(self):
        return '<article {}>'.format(self.title)