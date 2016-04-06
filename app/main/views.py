from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from ..email import send_email
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from flask.ext.login import login_required

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

@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	return render_template('user.html', user=user)

@main.route('/edit-profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user)
		flash('Your profile has been updated.')
		return redirect(url_for('.user', username = current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', form = form)
