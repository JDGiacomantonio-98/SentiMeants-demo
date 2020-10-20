
def create_db():
	from flask import current_app

	from app import create_app, db
	from app.configs import set_config
	from tests import DBTester

	unittest = DBTester()
	with create_app(config=set_config(select=True)).app_context():
		db.init_app(current_app)
		unittest.init_app(app=current_app, db=db)
		if unittest.test_db_exist():
			unittest.test_db_connection()


def basic_usecase(query=None):
	from app.main.methods.api_engine import authenticate, extract_tweets_from_q

	api = authenticate()
	if query is not None:
		return extract_tweets_from_q(query=query, api=api)
	return extract_tweets_from_q(query=build_query_from_cl(), api=api)


def build_query_from_cl(target=None):
	import re

	while (not target) or (target is None) or (type(target) != str):
		print('* this field is required *')
		target = input('Word or phrase you are looking for (use commas to separate search words or phrases) : ')
		targets = set()
		for itm in target.split(sep=","):
			if not (re.search('[a-zA-Z]|[0-9]', itm)):
				continue
			for punctuation in re.findall('[.:;'"/]", itm):
				itm = itm.replace(punctuation, "")
			itm = itm.strip(" ")
			if " " in itm:  # then it is a phrase
				n_gram = ''
				for w in itm.split(sep=' '):
					if w != '':
						if n_gram == '':
							n_gram = w
						else:
							n_gram += f' {w}'
					itm = f'"{n_gram}"'
			targets.add(itm)
	print('* this field is optional *')
	for itm in input('Words to exclude (use commas to separate filters) :').split(sep=","):
		filters = set()
		if not (re.search('[a-zA-Z]|[0-9]', itm)):
			continue
		for punctuation in re.findall('[.:;'"/]", itm):
			itm = itm.replace(punctuation, "")
		itm = itm.strip(" ")
		if " " in itm:  # then it is a phrase
			n_gram = ''
			for w in itm.split(sep=' '):
				if w != '':
					if n_gram == '':
						n_gram = w
					else:
						n_gram += f' {w}'
				itm = f'"{n_gram}"'
		filters.add(itm)
	for i, t in enumerate(targets):
		if i == 0:
			target = t.lower()
		else:
			target += f' {t}'
	for i, t in enumerate(filters):
		if i == 0:
			filters = f' -{t.lower()}'
		else:
			filters += f' -{t.lower}'
	print(f'launched query : {target}{filters}')
	return f'{target}{filters}'


def func_speedtest(func, iterations=10, rtn_df=False, cl_label='completed in', **kwargs):
	from datetime import datetime as dt

	def wrapper(**kwargs):
		start = dt.now()
		res = func(**kwargs)
		return res, dt.now() - start

	try:
		wr_res = wrapper(**kwargs)
	except Exception as e:
		raise e
	else:
		if rtn_df:
			from pandas import DataFrame

			return DataFrame(data=[[func.__name__, wr_res[1]] for i in range(iterations)], columns=["function name", "run-time (s)"])
		print(f'{cl_label} : {wr_res[1]}\n')

		return wr_res[0]

