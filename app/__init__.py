from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from tests import DBTester, TwitterTester
from app.main.machine_learning_pipeline import TweetsClassificationPipeline
from devkit import func_speedtest

clp = TweetsClassificationPipeline()
sia = SentimentIntensityAnalyzer()

db = SQLAlchemy()
burner = Bcrypt()

DBTester = DBTester()
TwitterTester = TwitterTester()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app(config):

	print('++ --- NEW APP INSTANCE --- ++')
	print('\n** creating app ...')

	app = Flask(__name__)

	try:
		app.config.from_object(config)
		if app.config['SECRET_KEY'] is None:
			raise TypeError
		print(f"RUNNING CONFIG: {app.config['ENV']}")
	except Exception as e:
		print(f'\nThe application factory has been closed due to occurency of error: \n{e}.')
		return None
	else:
		db.init_app(app)
		try:
			if app.config['USE_MODEL']:
				try:
					func_speedtest(clp.init_app, app=app, iterations=1, cl_label='predictor ready in')
				except Exception as e:
					print('Loading ML model : failed\n')
					print(f'Error : {e}')
		except Exception as e:
			print(e)
		with app.app_context():
			DBTester.init_app(app, db)
			TwitterTester.init_app(app)
			# do whatever stuff needed to check the application is fully working
			print('running tests ...')

			if DBTester.test_db_ready() and TwitterTester.test_api_basic_usecase():
				print('All tests passed!')
				login_manager.init_app(app)
				burner.init_app(app)

				from app.main import main
				app.register_blueprint(main)

				from app.auth import auth
				app.register_blueprint(auth)

				from app.errors import errors
				app.register_blueprint(errors)

		return app
