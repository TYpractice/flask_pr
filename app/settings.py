import os
from pathlib import Path

basedir = os.path.dirname(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app.sqlite')

SECRET_KEY = os.urandom(10)

UPLOAD_FOLDER = str(Path(basedir,'app','images'))