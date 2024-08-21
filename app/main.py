from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_paginate import Pagination,get_page_parameter

app = Flask(__name__)

app.config.from_pyfile('settings.py')

"""
↓SQLAlchemyの登録
"""
db = SQLAlchemy()
db.init_app(app)

Migrate(app,db)


"""
↓LoginManagerの登録
"""

login_manager = LoginManager()
#↓初期ページもしくはログインページでもいいかも　
login_manager.login_view = 'index'
login_manager.login_message =''
login_manager.init_app(app)


# ↓「authapp」の登録

from app.authapp.views import authapp
app.register_blueprint(authapp,url_prefix = '/auth')

# ↓「blogapp」の登録
from app.blogapp.views import blogapp
app.register_blueprint(blogapp,url_prefix ='/picture')


"""
↓メインページへのルーティング
"""
from app.blogapp import models as modelblog

@app.route('/' , methods =['GET','POST'])
def index():
  stmt = select(modelblog.Userblog).order_by(modelblog.Userblog.create_at.desc())
  entries = db.session.execute(stmt).scalars().all()
  
  page = request.args.get(get_page_parameter(),type=int,default=1)
  display= entries[(page-1)*6: page*6]
  
  pagination = Pagination(
    page = page,
    total = len(entries),
    per_page = 6
  )
  return render_template('index.html',user_picts =display , pagination =pagination)

@app.route('/detail/<int:id>')
def detail(id):
  detail = db.session.get(modelblog.Userblog,id)
  return render_template('home_detail.html',detail=detail)