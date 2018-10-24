from webapp import celery
from webapp import app
from celery.exceptions import Ignore, MaxRetriesExceededError
from webapp.models import Regions
from celery import states
import os
import os.path
import pickle
import socket
import glob


# function for converting ip address format aaa.bbb.ccc.ddd to ccc-ddd format
def convert_id(ip2):
	ip_octets = ip2.split('.')
	evc_id= '*' + str(ip_octets[2]).rjust(3, '0') + '-' + str(ip_octets[3]).rjust(3, '0') + '*'
	return evc_id


# function for converting  serial number of registrator to IP
def make_service_ip(serial_id):
	serialip = []
	ip_octets = serial_id.split('-')
	for octet in ip_octets:
		while octet[0] == '0':
			octet = octet[1:]
		serialip.append(octet)
	ip_string = '10.5' + '.' + serialip[0] + '.' + serialip[1]
	return  ip_string

# function for converting ip address to adorXX_XXX format
def find_main_keys(main_ip):
	main_keys = []
	octets = main_ip.split('.')
	crtfile = app.config['MAIN_KEYS_DIR'] + "ador" + octets[2] + '_' + octets[3] + '.crt'
	keyfile = app.config['MAIN_KEYS_DIR'] + "ador" + octets[2] + '_' + octets[3] + '.key'
	cafile = app.config['MAIN_KEYS_DIR'] + 'ca.crt'
	main_keys.append(crtfile)
	main_keys.append(keyfile)
	main_keys.append(cafile)
	return main_keys

def find_evc_keys(ip2, region):
	reg = Regions.query.filter_by(name=region).first()
	evc_keys = glob.glob(os.path.join(app.config['EVC_KEYS_DIR'], reg.keys_dir, convert_id(ip2)))
	evc_keys.append(os.path.join(app.config['EVC_KEYS_DIR'], reg.keys_dir, 'ca.crt'))
	return evc_keys


@celery.task(bind=True)
def copy_main_keys(self, ip1):
	file_list = find_main_keys(ip1)
	for fl in file_list:
		#filesize = os.stat(fl).st_size
		handshake = pickle.dumps(('copy_prod_keys', os.path.basename(fl)))
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect(("10.10.1.15", 5566))

		except ConnectionRefusedError as err:
			if self.request.retries == 3:
				self.update_state(state=states.FAILURE, meta='Connection refused to remote host. Max attemts exceeded')
				raise Ignore()
				return
			else:
				raise self.retry(countdown=60, max_retries=3)
		sock.sendall(handshake)
		response = sock.recv(2).decode()
		if response == 'OK':
			file = open(fl, 'rb')
			data = file.read(1024)
			while data:
				sock.send(data)
				data = file.read(1024)
			file.close()
		sock.close()


@celery.task(bind=True)
def copy_evc_keys(self, ip2, region):
	file_list = find_evc_keys(ip2, region)
	reg = Regions.query.filter_by(name=region).first()
	for fl in file_list:
		handshake = pickle.dumps(('copy_evc_keys', reg.keys_dir, os.path.basename(fl)))
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect(("10.10.1.15", 5566))
		except ConnectionRefusedError as err:
			if self.request.retries == 3:
				self.update_state(state=states.FAILURE, meta='Connection refused to remote host. Max attemts exceeded')
				raise Ignore()
				return
			else:
				raise self.retry(countdown=60, max_retries=3)
		sock.sendall(handshake)
		response = sock.recv(2).decode()
		if response == 'OK':
			file = open(fl, 'rb')
			data = file.read(1024)
			while data:
				sock.send(data)
				data = file.read(1024)
			file.close()
		sock.close()

