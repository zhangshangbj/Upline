#! /bin/python
#-*- coding: utf-8 -*-


try:
	import MySQLdb
	import MySQLdb.cursors
	import fnmatch
	import re
	import os,sys
	import hashlib
	import subprocess
except ImportError:
	print "ImportError Moudle can\'t imported! Please install Upline and MySQL-python Packages!"

def __init__(self):
	self.filelist=[]
		
def fullrmdir(path):
	'''
删除整个目录
	'''
	for rdirs,sdirs,filename in os.walk(path):
		for name in filename:
			d=os.path.join(rdirs,name)
			os.remove(d)
	os.removedirs(path)

def Rmdir(path):
	'''
删除目录下的所有内容，但保留该目录
	'''
	stderr=subprocess.Popen('rm -rf %s/*' %(path),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stderr.readlines()
	print stderr

def Rm_all_files(path):
	'''
删除整个目录下的文件，但保留目录
	'''
	for rdirs,sdirs,filename in os.walk(path):
		for name in filename:
			d=os.path.join(rdirs,name)
			os.remove(d)

def partfile(srcpath):
	'''
返回指定目录下的文件列表，从子目录显示
	'''
	filelist=[]
	for root,dirs,files in os.walk(srcpath):
		for k in files:
			j=os.path.join(root,k).replace(srcpath,'')
			filelist.append(j)
	return filelist
		
def pathfile(srcpath):
	'''
返回指定目录下文件的列表，从根目录显示
	'''
	filelist=[]
	for root,dir2,file2 in os.walk(srcpath):
		for o in file2:
			j=os.path.join(root,o)
			filelist.append(j)
	return filelist		
		
class getmd5(object):
	'''
	m5加密各种
	'''	
	def __init__(self):
		self.dictfile={}
		self.md1=''
		self.filelist=[]
		
	def Get_Md5_Of_String(self,src):
		'''
		md5加密字符串
		'''
		self.md1 =hashlib.md5()
		self.md1.update(src)
		return self.md1.hexdigest() 

	def Get_Md5_Of_File(self,filename):
		'''
  		md5加密文件
  		'''
		if not os.path.isfile(filename):
			return
		self.myhash = hashlib.md5()
		f = file(filename,'rb')
		while True:
			b = f.read(8096)
			if not b :
				break
			self.myhash.update(b)
		f.close()
		return self.myhash.hexdigest()

	def Get_Md5_Of_Files(self,dir3):
		'''
  		批量用md5加密文件
  		'''
		self.filelist=pathfile(dir3)
		
		for k in self.filelist:
			Md=self.Get_Md5_Of_File(k)
			self.dictfile[k.replace(dir3, '').replace('//', '/')] = Md
		return self.dictfile


class Mysql_helper(object):
	def __init__(self,dbconf):
		self.mysql_dict = dbconf
		self.db = MySQLdb.connect(self.mysql_dict['host'],
								  self.mysql_dict['user'],
								  self.mysql_dict['passwd'],
								  self.mysql_dict['db'],
								  self.mysql_dict['port'],
								  cursorclass=MySQLdb.cursors.DictCursor,
								  charset="utf8"
								  )
		self.cursor = self.db.cursor()

	def _Select(self, column, table, where='1'):
		'''
        select * from admincharset="utf8"
        '''
		query = 'select ' + column + ' from ' + table + ' where ' + str(where)
		try:
			self.cursor.execute(query)
			self.cursor.scroll(0, mode='absolute')
			results = self.cursor.fetchall()
			return results
		except Exception, e:
			print e
		self.db.close()
		self.db.cursor.close()

	def _Delect(self, table, where):
		'''
        delete from admin where id=1
        '''
		query = 'delete from ' + table + ' where ' + where
		try:
			self.cursor.execute(query)
		except Exception, e:
			print e
		self.db.close()
		self.db.cursor.close()

	def _Update(self, table, set, where='1'):
		'''
        update admin set name='admin' where id=23
        '''
		query = 'update ' + table + ' set ' + set + ' where ' + where
		try:
			self.cursor.execute(query)
		except Exception, e:
			print e
		self.db.close()
		self.db.cursor.close()

	def _Insert(self, table, column, value):
		'''
        value = '"'+'value1'+'","'+'value2'+'"'
        _Insert(tablename,column,value)
        '''
		query = 'insert into ' + table + '(' + column + ') value (' + value + ')'
		try:
			self.cursor.execute(query)
		except Exception, e:
			print e
		self.db.close()
		self.db.cursor.close()