from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,length

"""
新規会員登録フォーム
"""

class Signup(FlaskForm):
  
  username = StringField(
    'ユーザ名',
    validators=[DataRequired(message='ユーザ名を入力してください'),length(max =20 , message='20文字以内で入力してください')]
  )
  
  email = StringField(
    'メールアドレス',
    validators=[DataRequired(message='メールアドレスを入力してください'),Email(message='メールアドレスの形式で入力してください')]
  )
  
  password = PasswordField(
    validators=[DataRequired(message='パスワード入力してください'),length(min=6 , message='6文字以上で設定し、入力してください')]
  )
  
  submit = SubmitField('新規登録')
  
"""
loginフォーム
"""

class LoginForm(FlaskForm):
  
  email = StringField(
    
    "メールアドレス",
    validators=[DataRequired(message='メールアドレスの入力が必要です'),
                Email(message='メールアドレスの形式での入力してください')]
  )
  
  password = PasswordField(
  
    "パスワード",
    validators=[DataRequired(message='パスワードの入力が必要です')]
  )
  
  submit = SubmitField("ログイン")
  