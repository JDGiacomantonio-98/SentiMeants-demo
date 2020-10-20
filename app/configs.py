from os import path, getenv

from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
	FLASKY_ADMIN = getenv('FLASKY_ADMIN')
	# needed to protect application from modifying cookies and cross site forgery request attacks
	# generated randomly by secret.token_hex(20)
	SECRET_KEY = getenv('FLASK_SECRET_KEY')
	PERMANENT = getenv('PERMANENT')
	PERMANENT_SESSION_LIFETIME = 1800
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	USE_MODEL = False


class DevConfig(Config):
	DEBUG = True
	USE_MODEL = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'dev.db')


class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'TEST.db')


class ProdConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')


config = {
	'development': DevConfig,
	'testing': TestConfig,
	'production': ProdConfig
}


def set_config(select=False):
	if select:
		return config[set_env(config_menu())]
	return config[set_env(selKey='d')]


def set_env(selKey):
	from os import path, getenv
	from dotenv import load_dotenv

	envs = {
		'd': 'development',
		't': 'testing',
		'p': 'production',
	}

	basedir = path.abspath(path.dirname(__file__))
	load_dotenv(path.join(basedir, '.env'))
	e = getenv('FLASK_ENV')
	if e is None:
		with open(path.join(basedir, '.env'), 'a') as f:
			f.write(f'\nFLASK_ENV={envs[selKey]}')
			return envs[selKey]
	elif e != envs[selKey]:
		with open(path.join(basedir, '.env'), 'r') as f:
			lines = f.readlines()
		with open(path.join(basedir, '.env'), 'w') as f:
			for line in lines:
				if 'FLASK_ENV=' in line:
					f.write(f'FLASK_ENV={envs[selKey]}')
				else:
					f.write(line)
	return envs[selKey]


def config_menu():
	# print a menu to create different instances of app working with different Configs profiles
	choices = ['', 'd', 't', 'p', 'q']
	print('==================')
	k = str(input('SELECT APP ENV (on this machine)\n'
				  '==================\n'
				  '[D]evelopment\n'
				  '[T]esting\n'
				  '[P]roduction\n\n'
				  '[Q]uit process\n'
				  'press < Enter > to run Defaults :\t'
				  )
			).lower()
	while k.isnumeric() or (k not in choices):
		print('Invalid input : please choose from menu options.')
		k = str(input('SELECT APP ENV (on this machine)\n'
					  '==================\n'
					  '[D]evelopment\n'
					  '[T]esting\n'
					  '[P]roduction\n\n'
					  '[Q]uit process\n'
					  'press < Enter > to run Defaults :\t'
					  )
				).lower()
	if k == 'q':
		quit()
	if k == '':
		k = 'd'
	return k
