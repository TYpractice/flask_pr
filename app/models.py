from datetime import datetime
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import UserMixin
from app.main import db,login_manager

class User(db.Model , UserMixin):
  
  """
  ユーザの新規登録テーブル
  テーブル名→users
  id→id（主キー,自動連番）
  username→ユーザ名(登録必須+20文字まで登録可)
  email→メールアドレス(登録必須＋ユニークキーを設定)
  password →パスワード(登録必須＋ハッシュ化して登録)
  create_at →登録日時
  """
  
  __tablename__ ='users'
  
  id = db.Column(
    db.Integer,
    primary_key = True,
    autoincrement = True
  )
  
  username = db.Column(
    db.String(20),
    index = True,
    nullable = False
  )
  
  email = db.Column(
    db.String,
    index = True,
    unique = True,
    nullable = False
  )
  
  password_hash = db.Column(
    db.String,
    nullable=False
  )
  
  create = db.Column(
    db.DateTime,
    default = datetime.now
  )
  
  
  # パスワードをハッシュ化 プロパティを直接参照された場合はエラーを表示
  
  @property
  def password_set(self):
    
    raise AttributeError('パスワードの読み取り不可です')
  
  @password_set.setter
  def password(self,password):
    self.password_hash = generate_password_hash(password)
    
  
  # メールアドレスの重複チェック
  
  def duplication_email(self):
    dp_check = User.query.filter_by(email=self.email).first() is not None
    return dp_check
  
  
  # ログイン時のパスワードの照合
  
  def verify_password(self,password):
    return check_password_hash(self.password_hash,password)
  

@login_manager.user_loader
def load_user(user_id):
  
  return db.session.get(User, user_id)