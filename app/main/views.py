from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from ..email import send_email
from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.name.data).first()
		if user is None:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
			if current_app.config['FLASKY_ADMIN']:
				print 'FLASKY_ADMIN IS SET: SEND MAIL NOW.'
				print 'current_app.config[flasky_admin] = %s' % current_app.config['FLASKY_ADMIN']
				print 'user = %s' % user
				send_email(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user = user)
		else:
			session['known'] = True
		session['name'] = form.name.data
		print 'session[name] = %s' % session['name']
		return redirect(url_for('.index'))
	return render_template('index.html', 
			form = form, name = session.get('name'),
			known = session.get('known', False),
			current_time = datetime.utcnow())
