from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Length

class NameForm(Form):
	name = StringField('what is your name?', validators = [Required()])
	submit = SubmitField('submit')

class EditProfileForm(Form):
	name = StringField('real name', validator=[Length(0, 64)])
	location = StringField('Location', validator=[Length(0, 64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')
