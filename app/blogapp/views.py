from flask import Blueprint,redirect,render_template,url_for,current_app,request,send_from_directory
from flask_login import login_required,logout_user,current_user
from sqlalchemy import select
from flask_paginate import Pagination,get_page_parameter
import uuid
from pathlib import Path
from app.main import db
from app.blogapp import forms
from app.blogapp import models as modelblog



blogapp = Blueprint(
  'blogapp',
  __name__,
  template_folder='blog_templates',
  static_folder= 'blog_static'
)

"""
↓blogapp内のルーティング
"""

# ログイン後のトップページへのルーティング
@blogapp.route('/' , methods =['GET','POST'])
@login_required
def index():
  stmt = select(modelblog.Userblog).order_by(modelblog.Userblog.create_at.desc())
  entries = db.session.execute(stmt).scalars().all()
  
  page = request.args.get(get_page_parameter(),type=int,default=1)
  display = entries[(page-1)*6: page*6]
  
  pagination = Pagination(
    page = page,
    total = len(entries),
    per_page = 6
  )
  
  return render_template('logined_index.html',user_picts =display , pagination = pagination)

# 画像フォルダ内の画像を返す（投稿した画像）
@blogapp.route('/image/<path:filename>')
def image_file(filename):
  
  return send_from_directory(current_app.config['UPLOAD_FOLDER'],filename)


# 詳細ページへのルーティング（ログイン後閲覧可能な詳細ページ）
@blogapp.route('/detail/<int:id>')
@login_required
def detail(id):
  detail = db.session.get(modelblog.Userblog,id)
  return render_template('detail.html',detail=detail)


# マイページへのルーティング
@blogapp.route('/mypage/<int:user_id>',endpoint='mypage')
@login_required
def mypage(user_id):
  
  stmt = select(modelblog.Userblog).filter_by(user_id = user_id).order_by(modelblog.Userblog.create_at.desc())
  mylist = db.session.execute(stmt).scalars().all()
  
  page = request.args.get(get_page_parameter(),type=int,default=1)
  display = mylist[(page-1)*6: page*6]
  
  pagination = Pagination(
    page = page,
    total = len(mylist),
    per_page = 6
  )
  
  return render_template('mypage.html' , mylist = mylist , user_picts=display , pagination=pagination)

# 投稿削除ルーティング
@blogapp.route('/delete/<int:id>')
@login_required
def delete(id):
  
  entry = db.session.get(modelblog.Userblog,id)
  db.session.delete(entry)
  db.session.commit() 
  
  return redirect(url_for('blogapp.mypage',user_id=current_user.id))

# 編集ページのルーティング
@blogapp.route('/edit/<int:id>',methods = ['GET','POST'])
@login_required
def edit(id):
  
  entry = db.session.get(modelblog.Userblog,id)
  form = forms.editblogupForm()
  
  if form.validate_on_submit():
    
    file = form.image.data
    suffix = Path(file.filename).suffix
    imagefile_uuid = str(uuid.uuid4())+suffix
    image_path = Path(current_app.config['UPLOAD_FOLDER'],imagefile_uuid)
    file.save(image_path)
    
    
    entry.user_id = current_user.id
    entry.username = current_user.username
    entry.title = form.title.data
    entry.contents = form.contents.data
    entry.image_path = imagefile_uuid

    db.session.commit()

    return redirect(url_for('blogapp.mypage',user_id=current_user.id))
  
  return render_template('edit.html' ,form = form , entry = entry)
  
# ログアウトのルーティング
@blogapp.route('/logout')
@login_required
def logout():
  logout_user()
  
  return redirect(url_for('index'))

# ブログ投稿ページへのルーティング
@blogapp.route('/upload' , methods = ['GET','POST'])
@login_required
def upload():
  form = forms.blogupForm()
  
  if form.validate_on_submit():
    
    file = form.image.data
    suffix = Path(file.filename).suffix
    imagefile_uuid = str(uuid.uuid4())+suffix
    image_path = Path(current_app.config['UPLOAD_FOLDER'],imagefile_uuid)
    file.save(image_path)
    
    up_data = modelblog.Userblog(
      
      user_id = current_user.id,
      username = current_user.username,
      title = form.title.data,
      contents = form.contents.data,
      image_path = imagefile_uuid
    )
    
    db.session.add(up_data)
    db.session.commit()
    
    return redirect(url_for('blogapp.mypage'))
  return render_template('upload.html' , form = form)
    
  
  





