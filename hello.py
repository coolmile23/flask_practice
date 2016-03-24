#!/usr/bin/python

# -*- coding:utf-8 -*-

from flask import Flask
from flask import render_template
from flask import url_for
from flask import session
from flask import redirect
from flask import flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
	name = StringField('What is you name?', validators=[Required()])
	submit = SubmitField('Submit')


app = Flask(__name__)
app.debug = True
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'This key is hard to guess'

@app.route('/user/<name>')
def user(name):
	return render_template("user.html", name=name)

@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'))	
@app.route('/base')
def base():
	return render_template('base.html')
@app.route('/new')
def new():
	return render_template('new.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

if __name__ == '__main__':
	manager.run()
