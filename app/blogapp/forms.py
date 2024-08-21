from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,length
from flask_wtf.file import FileField,FileAllowed,FileRequired

class blogupForm(FlaskForm):
  
  title = StringField(
    "タイトル",
    validators=[DataRequired(message="タイトルの入力が必要です"),length(max=100,message='100文字以内で入力してください'),]
  )
  
  contents= TextAreaField(
    "本文",
    validators=[DataRequired(message='内容を入力してください')]
  )
  
  image = FileField(
    validators=[FileRequired('画像ファイルを選択してください'),FileAllowed(['png','jpg','jpeg'],'サポートされていないファイル形式です')]
  )
  
  submit = SubmitField('投稿する')
  

class editblogupForm(FlaskForm):
  
  title = StringField(
    "タイトル",
    validators=[DataRequired(message="タイトルの入力が必要です"),length(max=100,message='100文字以内で入力してください'),]
  )
  
  contents= TextAreaField(
    "本文",
    validators=[DataRequired(message='内容を入力してください')]
  )
  
  image = FileField(
    validators=[FileRequired('画像ファイルを選択してください'),FileAllowed(['png','jpg','jpeg'],'サポートされていないファイル形式です')]
  )
  
  submit = SubmitField('編集する')