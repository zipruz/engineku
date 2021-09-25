import pymysql
from netaddr import IPAddress
import time
import json
import os 

serverdb='localhost'
userdb='root'
passworddb=''
db='ci_base'
table=''

def monitoringexe(sintak):
	connection = pymysql.connect(host=serverdb,user=userdb,password=passworddb,database=db,charset='utf8mb4',autocommit=True)
	try:
		with connection.cursor() as cur:
			cur.execute(sintak)
			data = cur.fetchall()

		return data
	finally:
	    connection.close()

def updateexec(table,idnyo):
	connection = pymysql.connect(host=serverdb,user=userdb,password=passworddb,database=db,charset='utf8mb4',autocommit=True)
	cursor = connection.cursor()
	sintak = "UPDATE `%s` SET `exe` = '0' WHERE `id` = %s;" %(table, idnyo)
	cursor.execute(sintak)
	cursor.close()
	connection.close()

def hapusexec(table,idnyo):
	connection = pymysql.connect(host=serverdb,user=userdb,password=passworddb,database=db,charset='utf8mb4',autocommit=True)
	cursor = connection.cursor()
	sintak = "DELETE FROM `%s` WHERE `id` = %s" %(table, idnyo)
	cursor.execute(sintak)
	cursor.close()
	connection.close()

def sintaknyo(sintak):
	connection = pymysql.connect(host=serverdb,user=userdb,password=passworddb,database=db,charset='utf8mb4',autocommit=True)
	cursor = connection.cursor()
	cursor.execute(sintak)
	cursor.close()
	connection.close()

step=1

while 1:

	datas=monitoringexe('SELECT id,ip,aksi,status,exe,old FROM `box_wb_list` WHERE exe=1')
	for data in datas:
		print("%s. STEP KE-%s"%(step,step))

		idnyo=data[0]
		ip=data[1]
		aksi=data[2]
		status=data[3]
		exe=data[4]
		old=data[5]  #ip,aksi,status
		ada=1

		if aksi==1:
			action="ACCEPT"
		else:
			action="DROP"

		# print(idnyo,ip,status)
		if(status==10):	
			print ("Hapus FW ID: %s" %(idnyo))
			iptables="iptables -D INPUT -s %s -j %s" %(ip,action)
			sintak="%s" %(iptables)
		elif(status==1):
			print ("Buat FW ID: %s" %(idnyo))
			iptables="iptables -A INPUT -s %s -j %s" %(ip,action)
			sintak="%s" %(iptables)
		elif(status==2):
			print ("EDIT ID: %s" %(idnyo))
			dataold = json.loads(old)	

			######DATA DARI FIELD OLD
			ipold=dataold['ip']
			if dataold['aksi']=='1':
				actionold="ACCEPT"
			else:
				actionold="DROP"

			iptables="iptables -D INPUT -s %s -j %s; iptables -A INPUT -s %s -j %s" %(ipold,actionold,ip,action)
			sintak="%s" %(iptables)

		elif(status==100):
			sintak="DELETE DB DAN DELETE FW ID: %s" %(idnyo)
			hapusexec('box_wb_list',idnyo)
			ada=0
		else:
			sintak="NOP"

		if(ada):
			updateexec('box_wb_list',idnyo)

		
		print(sintak)
		print("")
		step=step+1;

	time.sleep(1)