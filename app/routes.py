#从app模块中即从__init__.py中导入创建的app应用
import os

from flask import render_template, flash, redirect, url_for, request, make_response
from app import app
#导入表单处理方法
from forms import LoginForm

from flask_login import current_user, login_user
from app.models import User,  Submit
from flask_login import logout_user
from flask_login import login_required

from app import db
from forms import RegistrationForm

from datetime import datetime
from flask import abort, send_from_directory

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

#进主页
@app.route('/')
@app.route('/index')
@login_required  #这样，必须登录后才能访问首页了,会自动跳转至登录页
def index():


    return render_template('index.html',title = '我的')

#注册函数
@app.route('/login',methods=['GET','POST'])
def login():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    #创建一个表单实例
    form = LoginForm()
    # 对表格数据进行验证
    if form.validate_on_submit():
        # 根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
        user = User.query.filter_by(username=form.username.data).first()
        # 判断用户不存在或者密码不正确
        if user is None or not user.check_password(form.password.data):
            # 如果用户不存在或者密码不正确就会闪现这条信息
            flash('无效的用户名或密码')
            # 然后重定向到登录页面
            return redirect(url_for('login'))
        # 这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='登录', form=form)


#登出函数
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


#查看提交列表
@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():

    submits = Submit.query.all()

    return render_template('submited_work.html', submits=submits)


#下载功能
@app.route('/download/<filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    directory = os.getcwd()#文件目录
    if os.path.isfile(os.path.join(directory, filename)):
        response = make_response(
            send_from_directory(directory, filename.encode('utf-8').decode('utf-8'), as_attachment=True))

        #将utf8编码的中文文件名默认转为latin-1编码
        #避免中文文件名报错
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
        return response


    submits = Submit.query.all()
    return render_template('submited_work.html', submits=submits)



