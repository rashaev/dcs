from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from webapp import db, login_manager



class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def get_password_hash(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return  self.username

class Role(UserMixin, db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return self.name

class Registrator(db.Model):
	__tablename__ = 'registrator'
	serial_num = db.Column(db.String(12), primary_key=True, index=True)
	ip_main = db.Column(db.String(15), unique=True, nullable=False)
	ipm_evc = db.Column(db.String(15))
	reg_id = db.Column(db.String(7), nullable=False, unique=True)
	region = db.Column(db.String(), db.ForeignKey('regions.name'))

	def __repr__(self):
		return self.serial_num

class regions(db.Model):
	__tablename__ = 'regions'
	name = db.Column(db.String(30), primary_key=True)
	src_evc_key = db.Column(db.String(120))
	dst_evc_keys = db.Column(db.String(120))
	src_prod_keys = db.Column(db.String(120))
	dst_prod_keys = db.Column(db.String(120))
	registrators = db.relationship('Registrator', backref='region_', lazy='dynamic')

	def __repr__(self):
		return self.name


@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

def choice_role():
	return Role.query

def choice_region():
	return regions.query