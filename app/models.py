from datetime import datetime
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(64), nullable=False, unique=True, index=True)
  username = db.Column(db.String(64), nullable=False, unique=True, index=True)
  is_admin = db.Column(db.Boolean)
  password_hash = db.Column(db.String(128))
  name = db.Column(db.String(64))
  location = db.Column(db.String(64))
  bio = db.Column(db.Text())
  member_since = db.Column(db.DateTime(), default=datetime.utcnow)
  avatar_hash = db.Column(db.String(32))
  
  def is_active(self):
    return True

  def get_id(self):
    return self.id

  def is_authenticated(self):
    return True

  def is_anonymous(self):
    return False

  @property
  def password(self):
    raise AttributeError('password is not a readable attribute')
  
  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  @login_manager.unauthorized_handler
  def unauthorized():
    return Response('Please sign in to use BackPack', 401)
