import pymysql
from netaddr import IPAddress
import time
import os 

serverdb='localhost'
userdb='root'
passworddb='123321'
db='ci_base'
table='box_network'

def monitoringipadd():
	connection = pymysql.connect(host=serverdb,user=userdb,password=passworddb,database=db,charset='utf8mb4',autocommit=True)

	try:
		with connection.cursor() as cur:
			cur.execute('SELECT id, ip, mask, box_interface.device FROM `box_network` INNER JOIN box_interface ON box_network.id_interface = box_interface.int WHERE exe=1 and status=1')
			data = cur.fetchall()

		return data
	finally:
	    connection.close()


def monitoringipdel():
	connection = pymysql.connect(host=serverdb,user=userdb,password=passworddb,database=db,charset='utf8mb4',autocommit=True)

	try:
		with connection.cursor() as cur:
			cur.execute('SELECT id, ip, mask, box_interface.device FROM `box_network` INNER JOIN box_interface ON box_network.id_interface = box_interface.int WHERE exe=1 and status=0')
			data = cur.fetchall()

		return data
	finally:
	    connection.close()

def updateexec(idnyo):
	connection = pymysql.connect(host=serverdb,user=userdb,password=passworddb,database=db,charset='utf8mb4',autocommit=True)
	cursor = connection.cursor()
	sintak = "UPDATE `box_network` SET `exe` = '0' WHERE `box_network`.`id` = %s;" %(idnyo)
	cursor.execute(sintak)
	cursor.close()
	connection.close()



while 1:
	# print(f'Data: {monitoringipadd()[2]}')

	datas=monitoringipadd()

	for data in datas:
		idnyo=data[0]
		ip=data[1]
		mask=IPAddress(data[2]).netmask_bits()
		device=data[3]
		# sintak="ID: %s, IP: %s, Mask: %s, Device: %s"%(idnyo, ip, mask, device)
		# ip addr add 192.168.2.105/24 dev enp0s3
		# sintak="ifconfig %s %s netmask %s" %(device, ip, mask)
		sintak="ip addr add %s/%s dev %s" %(ip, mask, device)

		updateexec(idnyo)
		print(sintak)

	datas=monitoringipdel()
	for data in datas:
		idnyo=data[0]
		ip=data[1]
		mask=IPAddress(data[2]).netmask_bits()
		device=data[3]
		# sintak="ID: %s, IP: %s, Mask: %s, Device: %s"%(idnyo, ip, mask, device)
		# ip addr add 192.168.2.105/24 dev enp0s3
		# sintak="ifconfig %s %s netmask %s" %(device, ip, mask)
		sintak="ip addr del %s/%s dev %s" %(ip, mask, device)

		updateexec(idnyo)
		print(sintak)

	time.sleep(1)
