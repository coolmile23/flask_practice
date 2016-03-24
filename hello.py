#!/usr/bin/python

# -*- coding:utf-8 -*-

from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime


app = Flask(__name__)
app.debug = True
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/user/<name>')
def user(name):
	return render_template("user.html", name=name)

@app.route('/')
def index():
	return render_template('index.html', current_time=datetime.utcnow())	
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
