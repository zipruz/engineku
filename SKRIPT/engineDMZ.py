

import pymysql
from netaddr import IPAddress
import time
import json
import os 

serverdb='localhost'
userdb='root'
passworddb='123321'
db='ci_base'
table='box_pat'

def monitoringexe(sintak):
	connection = pymysql.connect(host=serverdb,user=userdb,password=passworddb,database=db,charset='utf8mb4',autocommit=True)
	try:
		with connection.cursor() as cur:
			cur.execute(sintak)
			data = cur.fetchall()

		return data
	finally:
	    connection.close()

def updateexec(idnyo):
	connection = pymysql.connect(host=serverdb,user=userdb,password=passworddb,database=db,charset='utf8mb4',autocommit=True)
	cursor = connection.cursor()
	sintak = "UPDATE `%s` SET `exe` = '0' WHERE `id` = %s;" %(table, idnyo)
	cursor.execute(sintak)
	cursor.close()
	connection.close()

def hapusexec(idnyo):
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


# /usr/sbin/iptables -t nat -A PREROUTING -p tcp --dport 8291 -j DNAT --to 192.168.0.10:8291
# /usr/sbin/iptables -A FORWARD -p tcp --dport 8291 -d 192.168.0.10 -j ACCEPT

step=1

while 1:

	datas=monitoringexe("SELECT id, protokol, src_ip, src_port, dst_ip, dst_port, status, old, exe FROM `%s` WHERE exe=1" %(table))
	for data in datas:

		idnyo=data[0]
		protokol=data[1]
		src_ip=data[2]
		src_port=data[3]
		dst_ip=data[4]
		dst_port=data[5]
		status=data[6]
		old=data[7]
		exe=data[8]

		print("%s. STEP KE-%s"%(step,idnyo))
		

		ada=1

		action="ACCEPT"
		sintak=''

		# print(idnyo,ip,status)
		if(status==10):	
			print ("Hapus DMZ ID: %s" %(idnyo))
			# iptables="iptables -D INPUT -s %s -j %s" %(ip,action)
			# sintak="%s" %(iptables)
		elif(status==1):
			print ("Buat DMZ ID: %s" %(idnyo))
			# iptables="iptables -A INPUT -s %s -j %s" %(ip,action)
			# sintak="%s" %(iptables)
		elif(status==2):
			print ("EDIT DMZ ID: %s" %(idnyo))
			dataold = json.loads(old)	

			# ######DATA DARI FIELD OLD
			# ipold='x'
			
			# actionold="ACCEPT"
			
			# iptables="iptables -D INPUT -s %s -j %s; iptables -A INPUT -s %s -j %s" %(ipold,actionold,ip,action)
			# sintak="%s" %(iptables)

		elif(status==100):
			sintak="DELETE DB DAN DELETE DMZ ID: %s" %(idnyo)
			hapusexec(idnyo)
			ada=0
		else:
			sintak="NOP"

		if(ada):
			updateexec(idnyo)

		
		print(sintak)
		print("")
		step=step+1;

	time.sleep(1)