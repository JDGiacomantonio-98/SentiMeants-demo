from flask import redirect, url_for, render_template, request, session, flash, abort
from flask_login import current_user, login_user, logout_user, login_required

from app import db
from app.dbModels import User
from app.auth import auth
from app.auth.methods import powderize, reidrate_hash
from app.auth.forms import AccessDoorForm


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if current_user.is_authenticated:
		flash('You already have an active account on Seantimeant!', 'secondary')
		return redirect(url_for('main.home'))
	form = AccessDoorForm(login=False)
	if request.method == 'POST':
		if form.validate():
			try:
				db.session.add(User(email=form.email.data, psw=powderize(form.password.data)))
				db.session.commit()
			except Exception as e:
				db.session.rollback()
				return redirect(url_for('errors.raise_generic', error=e))
			else:
				flash('WOW, your account has been created successfully!', 'success')
				flash('Please check your email box and click on the link we sent to you to unlock Sentimeant powers!', 'warning')
				return redirect(url_for('auth.login'))
		flash('Please check your entries.', 'danger')
	return render_template('auth/sign_up.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		flash('You are already logged into Seantimeant!', 'secondary')
		return redirect(url_for('main.set_host', host='client'))
	form = AccessDoorForm()
	if request.method == 'POST':
		if form.validate():
			itm = User.query.filter_by(email=form.email.data).first()
			if itm:
				if reidrate_hash(itm.psw, form.password.data):
					login_user(itm)
					return redirect(url_for('main.set_host', host='client'))
				flash('Wrong email or password. Please check your input', 'danger')
				return render_template('auth/login.html', form=form)
			flash('The email address provided do not match any of our user.', 'warning')
		flash('Wrong email or password. Please check your input', 'danger')
	return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.home'))
