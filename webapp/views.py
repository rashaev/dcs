from webapp import app, db
from flask import  render_template, url_for, redirect, session, flash, request
from webapp.forms import LoginForm, AddUser, ServiceWork, AddRegion
from werkzeug.security import generate_password_hash
from webapp.models import User, Role, Registrator, Regions
from flask_login import login_required, login_user, current_user, logout_user
from functools import wraps
from webapp.tables import RegistratorTable, RegionTable, UserTable
from sqlalchemy import exc
from webapp.tasks import *
import datetime


def admin_required(f):	
	@wraps(f)
	def wrapped(*args, **kwargs):
		if str(current_user.role) not in 'Administrator':
			flash('Требуются права администратора')
			return redirect(url_for('login', next=request.url))
		return f(*args, **kwargs)
	return wrapped
	


@app.route('/', methods = ['GET', 'POST'])
@login_required
def index():
	form = ServiceWork()
	items = Registrator.query.all()
	page = request.args.get('page', 1, type=int)
	pagination = Registrator.query.order_by(Registrator.serial_num).paginate(page, per_page=app.config['FLASKY_POSTS_PER_PAGE'], error_out=True)
	table = RegistratorTable(pagination.items)
	if form.validate_on_submit() and form.submit.data:
		ip1 = form.ip_addr_1.data
		if form.setup.data:
			copy_main_keys.delay(ip1)
		registrator = Registrator.query.filter_by(serial_num=form.serial_num.data).first()
		if registrator is None:
			new_reg = Registrator(serial_num=str(form.serial_num.data), ip_main=str(form.ip_addr_1.data), ipm_evc=str(form.ip_addr_2.data), reg_id=str(form.reg_id.data), region=str(form.region.data), created_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			try:
				db.session.add(new_reg)
				db.session.commit()
				flash('Регистратор %s добавлен' % form.serial_num.data, 'success')
			except (exc.IntegrityError) as error:
				if 'duplicate key value violates unique constraint' in error.args[0]:
					flash('Регистратор не был добавлен. Подробности в лог файле', 'warning')
			return redirect(url_for('index'))
		else:
			flash("Регистратор %s уже существует" % form.serial_num.data, 'warning')
	return render_template('index.html', table=table, pagination=pagination, form=form)


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
	items = User.query.all()
	table = UserTable(items)
	if form.validate_on_submit():
		roleid = db.session.query(Role.id).filter_by(name=str(form.role.data)).first()
		user = User(username=form.username.data, password_hash=generate_password_hash(form.password.data), role_id=roleid[0])
		db.session.add(user)
		db.session.commit()
		flash('Пользователь добавлен', 'success')
		items = User.query.all()
		table = UserTable(items)
	return render_template('add_user.html', form=form, table=table)

@app.route('/add_region', methods=['GET', 'POST'])
@login_required
@admin_required
def add_region():
	form = AddRegion()
	items = Regions.query.all()
	table = RegionTable(items)
	if form.validate_on_submit():
		region = Regions(name=form.name.data, keys_dir=form.keys_dir.data)
		db.session.add(region)
		db.session.commit()
		flash('Регион добавлен', 'success')
		items = Regions.query.all()
		table = RegionTable(items)
	return render_template('add_region.html', form=form, table=table)


@app.route('/registrator/<ser_num>', methods=['GET', 'POST'])
@login_required
def edit(ser_num):
	form = ServiceWork()
	registrator = Registrator.query.filter_by(serial_num=ser_num).first()
	if form.validate_on_submit():
		reg_edit = Registrator.query.filter_by(serial_num=str(ser_num)).update(dict(ip_main=str(form.ip_addr_1.data), ipm_evc=str(form.ip_addr_2.data), reg_id=str(form.reg_id.data), region=str(form.region.data), created_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		db.session.commit()
		flash('Регистратор %s успешно изменен' % registrator.serial_num, 'success')
		return redirect(url_for('index'))
	return render_template('registrator.html', form=form, registrator=registrator)

@app.route('/delete/<ser_num>', methods=['GET', 'POST'])
@login_required
def delete(ser_num):
	reg_del = Registrator.query.filter_by(serial_num=ser_num).delete()
	db.session.commit()
	flash('Регистратор %s удален' % ser_num, 'success')
	return redirect(url_for('index'))

@app.route('/delete_region/<name>', methods=['GET', 'POST'])
@login_required
def del_region(name):
	region_del = Regions.query.filter_by(name=name).delete()
	db.session.commit()
	flash('Регион %s удален' % name, 'success')
	return redirect(url_for('add_region'))

@app.route('/delete_user/<user_name>', methods=['GET', 'POST'])
@login_required
def del_user(user_name):
	user_del = User.query.filter_by(username=user_name).delete()
	db.session.commit()
	flash('Пользователь %s удален' %user_name, 'success')
	return redirect(url_for('add_user'))

@app.route('/logout') 
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))