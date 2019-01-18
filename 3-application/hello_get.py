#!/usr/bin/python  
import pymysql
import cgi, cgitb
import os,copy
form = cgi.FieldStorage()
name = form.getvalue('name')
passwd = form.getvalue('passwd')
sql = "insert into users (name,pass) values('{0}','{1}');".format(name,passwd)
print(sql)

db = pymysql.connect(host="localhost",user="root",password="123456",database="web",charset="utf8")
cursor = db.cursor()
sql = "insert into users (name,pass) values('{0}','{1}');".format(str(name),str(passwd))
cursor.execute(sql)
db.commit()
db.close()

print ("<h2>Hello {0}</h2>".format(name))  
 

