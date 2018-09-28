from flask_table import Table, Col, LinkCol


class RegistratorTable(Table):
	classes = ['table', 'table-bordered', 'table-sm', 'table-hover']
	thead_classes = ['thead-dark']
	serial_num = Col('Серийный номер')
	ip_main = Col('IP адрес(осн.)')
	ipm_evc = Col('IP адрес(евц)')
	reg_id = Col('Рег.id')
	region = Col('Регион')
	edit = LinkCol('edit', 'edit', url_kwargs=dict(serial_num='serial_num'))