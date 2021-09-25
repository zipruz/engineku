import pymysql
from netaddr import IPAddress
import time
import json
import os 



def monitoringfwdexe():
	con = pymysql.connect(host='localhost',user='root',password='',database='ci_base',charset='utf8mb4')

	try:
		with con.cursor() as cur:
			cur.execute('SELECT id, type, protokol, src_ip, src_port, dst_ip, dst_port, alertid, aksi, status, old FROM `box_firewall` WHERE exe=1')
			data = cur.fetchall()

		return data
	finally:
	    con.close()


def updateold(idnyo):
	connection = pymysql.connect(host='localhost',user='root',password='',database='ci_base',charset='utf8mb4',autocommit=True)
	cursor = connection.cursor()
	sintak = "UPDATE `box_firewall` SET `old` = '' WHERE `box_firewall`.`id` = %s;" %(idnyo)
	cursor.execute(sintak)
	cursor.close()
	connection.close()


def updateexec(idnyo):
	connection = pymysql.connect(host='localhost',user='root',password='',database='ci_base',charset='utf8mb4',autocommit=True)
	cursor = connection.cursor()
	sintak = "UPDATE `box_firewall` SET `exe` = '0' WHERE `box_firewall`.`id` = %s;" %(idnyo)
	cursor.execute(sintak)
	cursor.close()
	connection.close()

def hapusexec(idnyo):
	connection = pymysql.connect(host='localhost',user='root',password='',database='ci_base',charset='utf8mb4',autocommit=True)
	cursor = connection.cursor()
	sintak = "DELETE FROM `box_firewall` WHERE `box_firewall`.`id` = %s" %(idnyo)
	cursor.execute(sintak)
	cursor.close()
	connection.close()



step=1

while 1:
	# print(f'Data: {monitoringfwadd()}')

	datas=monitoringfwdexe()

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
		status=data[9]


		ada=1
		if(status==10):	
			sintak="Hapus FW %s/%s dev %s " %(src_ip, src_port, aksi)
		elif(status==1):			
			sintak="ADD FW %s/%s dev %s " %(src_ip, src_port, aksi)
		elif(status==2):	
			old=data[10]  #id,date,type,protokol,src_ip,src_port,dst_ip,dst_port,alertid,aksi,status,exe
			dataold = json.loads(old)		
			sintak="DELETE FW OLD:%s \nUPDATE ADD FW %s/%s dev %s " %(dataold['src_ip'],src_ip, src_port, aksi)
		elif(status==100):
			sintak="DELETE DB DAN DELETE FW %s/%s dev %s " %(src_ip, src_port, aksi)
			hapusexec(idnyo)
			ada=0
		else:
			sintak="NOP"

		if(ada):
			updateexec(idnyo)

		print("%s. STEP KE-%s"%(step,step))
		print(sintak)
		print("")
		step=step+1;



	time.sleep(1)
