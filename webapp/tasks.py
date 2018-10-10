from webapp import celery
from webapp import app
import os
import os.path
import pickle
import socket

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



@celery.task
def copy_main_keys(ip1):
	file_list = find_main_keys(ip1)
	for fl in file_list:
		filesize = os.stat(fl).st_size
		handshake = pickle.dumps((os.path.basename(fl), filesize))
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(("192.168.10.99", 5566))
		sock.send(handshake)
		response = sock.recv(2).decode()
		print(response)
		if response == 'OK':
			print("Transfer file", fl)
			file = open(fl, 'rb')
			data = file.read(filesize)
			print(len(data))
			sock.send(data)
			file.close()
			sock.close()