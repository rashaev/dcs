from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Regexp, Optional, IPAddress
from webapp.models import choice_role, choice_region, User

class LoginForm(FlaskForm):
	username = StringField('Login', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Войти')
	remember_me = BooleanField('Remember me')

class AddUser(FlaskForm):
	username = StringField('Login', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])
	password = PasswordField('Password', validators=[DataRequired(), Length(6, 12)])
	role = QuerySelectField(query_factory=choice_role, allow_blank=False)
	submit = SubmitField('Добавить')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Имя пользователя уже используется.')

class ServiceWork(FlaskForm):
	region = QuerySelectField(query_factory=choice_region, allow_blank=False)	
	ip_addr_1 = StringField('IP address', validators=[DataRequired(), IPAddress()])
	ip_addr_2 = StringField('IP address', validators = [Optional(), IPAddress()])
	reg_id = StringField('RegID', validators=[DataRequired()])
	serial_num = StringField('Serial number', validators = [DataRequired()])
	submit = SubmitField('Настроить')

class AddRegion(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	src_prod_keys = StringField('Source production keys', validators=[DataRequired()])
	dst_prod_keys = StringField('Destination production keys', validators=[DataRequired()])
	src_evc_keys = StringField('Source evc keys')
	dst_evc_keys = StringField('Destination evc keys')
	submit = SubmitField('Добавить')