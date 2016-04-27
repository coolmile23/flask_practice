#!/usr/bin/env python

import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
	import coverage
	COV = coverage.coverage(branch=True, include='app/*')
	COV.start()

from app import create_app, db
from app.models import User, Role, Post
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app = app, db = db, User = User, Role = Role,\
		 Post = Post, Permission=Permission, Follow=Follow,\
		Comment=Comment)

manager.add_command('shell', Shell(make_context = make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False):
	''' Run the unit tests. '''
	if coverage and os.environ.get('FLASK_COVERAGE'):
		import sys
		os.environ['FLASK_COVERAGE'] = '1'
		os.excepvp(sys.executable, [sys.executable] + sys.argv)
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity = 2).run(tests)
	if COV:
		COV.stop()
		COV.save()
		print('Coverage Summary:')
		COV.report()
		basedir = os.path.abspath(os.path.dirname(__file__))
		covdir = os.path.join(basedir, 'tmp/coverage')
		COV.hmtl_report(directory=covdir)
		print('HTML version: file://%s/index.html' % covdir)
		COV.erase()

@manager.command
def deploy():
	'''Run deployment tasks.'''
	from flask.ext.migrate import upgrade
	from app.models import Role, User

	# migrate to the newest version of database	
	upgrade()

	# create user Role
	Role.insert_roles()

	# let all user follow this user
	User.add_self_follows()


if __name__ == '__main__':
	manager.run()

