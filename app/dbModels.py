from flask_login import UserMixin

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)


class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True, index=True)
	confirmed = db.Column(db.Integer, nullable=False, default=0)
	email = db.Column(db.String(250), unique=True, nullable=False)
	psw = db.Column(db.String(128), nullable=False)

	def __repr__(self):
		return f'User Object {self.id} <{self.email}>'
