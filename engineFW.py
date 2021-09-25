import pymysql
from netaddr import IPAddress
import time
import json
import os 

def monitoringfwadd():
	con = pymysql.connect(host='localhost',user='root',password='',database='ci_base',charset='utf8mb4')

	try:
		with con.cursor() as cur:
			cur.execute('SELECT id, type, protokol, src_ip, src_port, dst_ip, dst_port, alertid, aksi, state FROM `box_firewall` WHERE state=0 and exe=1 and status=1')
			data = cur.fetchall()

		return data
	finally:
	    con.close()

def monitoringfwdel():
	con = pymysql.connect(host='localhost',user='root',password='',database='ci_base',charset='utf8mb4')

	try:
		with con.cursor() as cur:
			cur.execute('SELECT id, type, protokol, src_ip, src_port, dst_ip, dst_port, alertid, aksi FROM `box_firewall` WHERE exe=1 and status=0')
			data = cur.fetchall()

		return data
	finally:
	    con.close()


def monitoringfwupdate():
	con = pymysql.connect(host='localhost',user='root',password='',database='ci_base',charset='utf8mb4')

	try:
		with con.cursor() as cur:
			cur.execute('SELECT id, type, protokol, src_ip, src_port, dst_ip, dst_port, alertid, aksi, state, old FROM `box_firewall` WHERE state>0 and exe=1 and status>0')
			data = cur.fetchall()

		return data
	finally:
	    con.close()




def updateexec(idnyo):
	connection = pymysql.connect(host='localhost',user='root',password='',database='ci_base',charset='utf8mb4',autocommit=True)
	cursor = connection.cursor()
	sintak = "UPDATE `box_firewall` SET `exe` = '0' WHERE `box_firewall`.`id` = %s;" %(idnyo)
	cursor.execute(sintak)
	cursor.close()
	connection.close()



while 1:
	# print(f'Data: {monitoringfwadd()}')

	datas=monitoringfwadd()

	for data in datas:

		idnyo=data[0]
		typefw=data[1]
		protokol=data[2]
		src_ip=data[3]
		src_port=data[4]
		dst_ip=data[5]
		dst_port=data[6]
		alertid=data[7]
		aksi=data[8]

		if(aksi):
			sintak="Firewall Jalan  ACCEPT %s/%s dev %s" %(src_ip, src_port, aksi)
		else:
			sintak="Firewall Jalan  DROP %s/%s dev %s" %(src_ip, src_port, aksi)

		updateexec(idnyo)
		print(sintak)


	datas=monitoringfwupdate()

	for data in datas:

		idnyo=data[0]
		typefw=data[1]
		protokol=data[2]
		src_ip=data[3]
		src_port=data[4]
		dst_ip=data[5]
		dst_port=data[6]
		alertid=data[7]
		aksi=data[8]
		state=data[9]
		old=data[10]

		dataold = json.loads(old)

		if dataold['status'] == 1:
			sintak="Firewall Update DELETE dan Jalankan %s/%s dev %s : %s" %(src_ip, src_port, aksi, dataold['status'])
		else:
			sintak="Firewall Update Jalan %s/%s dev %s : %s" %(src_ip, src_port, aksi, dataold['status'])

		updateexec(idnyo)
		print(sintak)

	time.sleep(1)



	datas=monitoringfwdel()

	for data in datas:

		idnyo=data[0]
		typefw=data[1]
		protokol=data[2]
		src_ip=data[3]
		src_port=data[4]
		dst_ip=data[5]
		dst_port=data[6]
		alertid=data[7]
		aksi=data[8]

		sintak="Firewall DELETE %s/%s dev %s" %(src_ip, src_port, aksi)

		updateexec(idnyo)
		print(sintak)

	time.sleep(1)
