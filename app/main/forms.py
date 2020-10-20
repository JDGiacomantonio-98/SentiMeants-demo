import re

from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
	target = StringField('Targets', validators=[DataRequired()], render_kw={'placeholder': 'use commas to separate search items'})
	filters = StringField('Filters', render_kw={'placeholder': 'use commas to separate excluded items'})

	submit = SubmitField()

	def __init__(self, submit_label=None, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		if submit_label is None:
			self.submit.label.text = 'Discover'
		elif type(submit_label) == str:
			self.submit.label.text = submit_label
		else:
			raise TypeError

	def build_query(self):
		# parsing of target/filter fields and addition of proper query symbols to customize search
		return f'{self.parse(self.target)}{self.parse(self.filters)}'

	@staticmethod
	def parse(field):
		if field.data != '':
			tokens = set()
			for itm in field.data.split(sep=","):
				if not(re.search('[a-zA-Z]|[0-9]', itm)):
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
				tokens.add(itm)
			for i, t in enumerate(tokens):
				if i == 0:
					itm = t if field.name == 'target' else f' -{t}'
				else:
					itm += f'{" " if field.name == "target" else " -"}{t}'
			return itm.lower()
		return ''
