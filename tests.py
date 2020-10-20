import unittest
from os import path

from devkit import basic_usecase
from app.main.methods.sentiment_engine import analyze_sentiments


class TwitterTester(unittest.TestCase):

	def __init__(self, app=None, api=None):
		super().__init__()
		self.app = app
		self.api = api

	def init_app(self, app, api=None):  # per app-instance init of the tester
		self.app = app
		self.api = api

	def test_api_basic_usecase(self):
		if self.test_api_auth():
			if self.test_api_getScores():
				return True
		return False

	def test_api_auth(self):
		try:
			self.test_api_getScores()  # authentication instructions
		except:
			return False
		else:
			return True

	def test_api_getScores(self):
		try:
			# tweets_df_sentiment = analyze_sentiments(basic_usecase())
			pass
		except:
			return False
		else:
			return True


class DBTester(unittest.TestCase):

	def __init__(self, app=None, db=None):
		super().__init__()
		self.app = app
		self.db = db

	def init_app(self, app, db):
		self.app = app
		self.db = db

	def test_db_ready(self):
		print('testing database ...')
		if self.test_db_exist():
			if self.test_db_connection():
				return True
		return False

	def test_db_exist(self):
		if 'sqlite:///' in self.app.config['SQLALCHEMY_DATABASE_URI']:
			if path.exists(self.app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')):
				return True
			print('(!) warning : No active db has been detected for the current working app.')
			if input('Do you want to create a brand new instance of the database? (y/n)') in ('y, Y'):
				self.db.create_all()
				self.test_db_exist()
			return False

	def test_db_connection(self):
		if self.test_db_IO():
			print('CONNECTION ON : {}'.format(self.app.config['SQLALCHEMY_DATABASE_URI']))
			return True
		print('** database : failed connection (!)')
		print('(!) INFO  : have you run upgrade() from last migration file?')
		return False

	def test_db_IO(self):
		from sqlalchemy.exc import OperationalError

		try:
			if self.test_db_write():
				if self.test_db_read():
					return True
			return False
		except OperationalError as e:
			print(f'** database : IO test failed due to error {e}')
			print('********************************')
			print('Trying to fix the problem ...')
			print('** Rolling back the previous session ...')
			self.db.session.rollback()
			print('** Attempting to recreate the database ...')
			self.db.drop_all()
			self.db.create_all()
			print('** testing new connection ...')
			if self.test_db_ready():
				return True
			return False

	def test_db_write(self):
		from app.dbModels import User
		from sqlalchemy.exc import IntegrityError
		from app.auth.methods import powderize

		try:
			self.db.session.add(User(email='write_db@test.it', psw=powderize('password123456')))
			self.db.session.commit()
		except IntegrityError:
			self.db.session.rollback()
			self.db.session.delete(User.query.filter_by(email='write_db@test.it').first())
			self.db.session.commit()
			if self.test_db_write():
				return True
			return False
		except Exception as e:
			print(f'** database : writing test failed due to error {e}')
			raise e
		else:
			return True

	def test_db_read(self):
		from app.dbModels import User

		try:
			u = User.query.filter_by(email='write_db@test.it').first()
			if u:
				self.db.session.delete(u)
				self.db.session.commit()
				return True
			if User.query.first() is None:
				return False
			return True
		except Exception as e:
			print(f'** database : reading test failed due to error {e}')
			raise e


if __name__ == '__main__':
	unittest.main()
