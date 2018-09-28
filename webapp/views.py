from webapp import app, db
from flask import  render_template, url_for, redirect, session, flash, request
from webapp.forms import LoginForm, AddUser, ServiceWork
from werkzeug.security import generate_password_hash
from webapp.models import User, Role, Registrator
from flask_login import login_required, login_user, current_user, logout_user
from functools import wraps
from webapp.tables import RegistratorTable



'''
def admin_required(*roles):	
	def wrapper(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			if str(current_user.role) not in roles:
				flash('Требуются права администратора')
				return redirect(url_for('login', next=request.url))
			return f(*args, **kwargs)
		return wrapped
	return wrapper
'''

def admin_required(f):	
	@wraps(f)
	def wrapped(*args, **kwargs):
		if str(current_user.role) not in 'Administrator':
			flash('Требуются права администратора')
			return redirect(url_for('login', next=request.url))
		return f(*args, **kwargs)
	return wrapped
	


@app.route('/')
@login_required
def index():
	form = ServiceWork()
	items = Registrator.query.all()
	table = RegistratorTable(items)
	return render_template('index.html', form=form, table=table)


@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, remember=form.remember_me.data)
			if request.args.get('next') is None:
				 return redirect(url_for('index'))
			else:
				return redirect(request.args.get('next'))
		flash('Неверный логин или пароль')
	return render_template('login.html', form=form)


@app.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
	form = AddUser()
	total_users = User.query.all()
	if form.validate_on_submit():
		roleid = db.session.query(Role.id).filter_by(name=str(form.role.data)).first()
		user = User(username=form.username.data, password_hash=generate_password_hash(form.password.data), role_id=roleid[0])
		db.session.add(user)
		db.session.commit()
		flash('Пользователь добавлен')
		total_users = User.query.all()
	return render_template('add_user.html', form=form, total_users=total_users)

@app.route('/registrator/<serial_num>', methods=['GET', 'POST'])
@login_required
def edit(serial_num):
	return "Test"



@app.route('/logout') 
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))