from flask_table import Table, Col, ButtonCol


class RegistratorTable(Table):
	classes = ['table', 'table-sm', 'table-hover', 'w-100']
	thead_classes = ['thead-dark']
	serial_num = Col('Серийный номер')
	ip_main = Col('IP адрес(осн.)')
	ipm_evc = Col('IP адрес(евц)')
	reg_id = Col('Рег.id')
	region = Col('Регион')
	edit = ButtonCol('изменить', 'edit', url_kwargs=dict(ser_num='serial_num'), button_attrs={"class" : "btn btn-info btn-sm"})
	delete = ButtonCol('удалить', 'delete', url_kwargs=dict(ser_num='serial_num'), button_attrs={"class" : "btn btn-dark btn-sm"})