from flask_table import Table, Col, ButtonCol


class RegistratorTable(Table):
	classes = ['table', 'table-sm', 'table-hover', 'w-100']
	thead_classes = ['thead-dark']
	serial_num = Col('Серийный номер')
	ip_main = Col('IP адрес(осн.)')
	ipm_evc = Col('IP адрес(евц)')
	reg_id = Col('Рег.id')
	region = Col('Регион')
	created_date = Col('Дата создания')
	edit = ButtonCol('изменить', 'edit', url_kwargs=dict(ser_num='serial_num'), button_attrs={"class" : "btn btn-info btn-sm"})
	delete = ButtonCol('удалить', 'delete', url_kwargs=dict(ser_num='serial_num'), button_attrs={"class" : "btn btn-dark btn-sm"})

class RegionTable(Table):
	classes = ['table', 'table-sm', 'table-hover', 'w-100']
	thead_classes = ['thead-dark']
	name = Col('Регион')
	keys_dir = Col('Каталог')
	delete = ButtonCol('удалить', 'del_region', url_kwargs=dict(name='name'), button_attrs={"class" : "btn btn-dark btn-sm"})

class UserTable(Table):
	classes = ['table', 'table-sm', 'table-hover', 'w-100']
	thead_classes = ['thead-dark']
	username = Col('Логин')
	role = Col('Роль')
	delete = ButtonCol('удалить', 'del_user', url_kwargs=dict(user_name='username'), button_attrs={"class" : "btn btn-dark btn-sm"})