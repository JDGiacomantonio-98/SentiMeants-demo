from flask import render_template

from app.errors import errors


@errors.app_errorhandler(403)
def raise_403(error):
	return render_template('errors/403.html', title='error: 403 - you cannot do that'), 403


@errors.app_errorhandler(404)
def raise_404(error):
	return render_template('errors/404.html', title='error: 404 - page not found', error=error), 404


@errors.app_errorhandler(500)
def raise_500(error):
	return render_template('errors/500.html', title='error: 500 - what happened?', error=error), 500


@errors.route('/<caller_route>/work-in-progress')
def raise_wip(caller_route):
	return render_template('errors/wip.html'), 200


@errors.route('/errors/<error>')
def raise_generic(error):
	return render_template('errors/generic_error.html', e=error), 500

