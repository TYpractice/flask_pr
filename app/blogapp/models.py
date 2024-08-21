from datetime import datetime
from app.main import db

class Userblog(db.Model):
  
  """
  ユーザの投稿テーブル
  テーブル名→blog
  id→id（主キー,自動連番）
  user_id→ユーザ名（ユーザ登録テーブルusersのidを外部キーとして登録)
  username→ユーザネーム
  title→タイトル
  contents→コンテンツ（本文)
  create_at →登録日時
  """
  
  __tablename__ ='blog'
  
  id= db.Column(
    db.Integer,
    primary_key = True,
    autoincrement = True
  )
  
  user_id = db.Column(
    db.String,
    db.ForeignKey('users.id')
  )
  
  username = db.Column(
    db.String,
    index = True
  )
  
  title = db.Column(
    db.String
  )
  
  contents = db.Column(
    db.Text
  )
  
  image_path = db.Column(
    db.String
  )
  
  create_at = db.Column(
    db.DateTime,
    default = datetime.today()
  )