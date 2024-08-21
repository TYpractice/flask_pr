from flask import Blueprint,render_template,redirect,url_for,flash
from flask_login import login_user
from sqlalchemy import select
from app.authapp import forms
from app import models
from app.main import db

authapp = Blueprint(
  'authapp',
  __name__,
  template_folder='templates_auth',
  static_folder='static_auth'
)

"""
↓新規登録＋ログインのルーティング 
"""

# 新規会員登録のルーティング
@authapp.route('/signup',methods =['GET','POST'])
def signup():
  
  form = forms.Signup()
  
  if form.validate_on_submit():
    
    user = models.User(
      
      username = form.username.data,
      
      email = form.email.data,
      
      password = form.password.data
    )
    
    if user.duplication_email():
      
      flash('登録済みのメールアドレスです')
      return redirect(url_for('authapp.signup'))
    
    db.session.add(user)
    db.session.commit()
    
    return redirect(url_for('authapp.login'))
  
  return render_template('signup.html' ,form = form)


# ログインのルーティング
@authapp.route('/login', methods =['GET','POST'])
def login():
  
  form = forms.LoginForm()
  
  if form.validate_on_submit():
    
    stmt =(
      select(models.User).filter_by(email=form.email.data).limit(1)
    )
    
    user = db.session.execute(stmt).scalars().first()
    
    if user is not None and user.verify_password(form.password.data):
      
      login_user(user)
      
      return redirect(url_for('blogapp.mypage',user_id = user.id))
    
    flash('メールアドレスまたはパスワードが間違っています')
    
  return render_template('login.html' , form = form)