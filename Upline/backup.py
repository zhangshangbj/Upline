#! /bin/python
#-*- coding: utf-8 -*-

'''
Backup the project to destination directory
'''

import time
import os
import sys
from shutil import copytree
from Upline.ctversion import version
from Upline.checkfile import dffile
from Upline.ParaSsh import ParmSsh

__metaclass__=type
class bkproject:
	def __init__(self):
		self.dateofnow=str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
		self.versionlist=[]

		self.Diff=dffile()
	def backup(self,projectpath,projectname,bakpath,flag='1.0'):
		'''
		备份
		:param projectpath: 工程目录
		:param projectname: 工程名
		:param bakpath:备份目录
		:param flag: 版本号
		:return:print 版本号
		'''
		srcpath=os.path.join(projectpath,projectname)
		bakpath=os.path.join(bakpath,projectname)
		try:
			self.versionlist=os.listdir(bakpath)
		except OSError:
			os.mkdir(bakpath,755)

		ver=version()
		Thisver=ver.mkversion(projectpath,projectname,flag)
		if Thisver == 'Err':
			print 'The version is too small. Backup failed'
			sys.exit(1)
		versn=os.path.join(bakpath,Thisver)
		copytree(srcpath,versn)
		Diff_file_list=self.Diff.dffoflist(srcpath,versn)
		if len(Diff_file_list) == 0:
			print ("Backup success! %s version=" %versn)
		else:
			print 'File bakup failed',Diff_file_list

	def Ssh_backup(self,hostname, username,projectpath,projectname,bakpath,flag='1.0'):
		'''
		备份
		:param projectpath: 工程目录
		:param projectname: 工程名
		:param bakpath:备份目录
		:param flag: 版本号
		:return:print 版本号
		'''
		print '------------------------ %s 备份原工程--------------------------' %(hostname)
		Ssh = ParmSsh(hostname, username)
		try:

			srcpath=os.path.join(projectpath,projectname)
			bakpath=os.path.join(bakpath,projectname)
			Ver_path=os.path.join(srcpath,'version')
			ver=version()
			Thisver=ver.Ssh_mkversion(projectpath,projectname,flag,'1')
			Ssh.Exe_cmd('touch %s' %(Ver_path))
			if Thisver == 'Err':
				raise SystemExit('The version is too small. Backup failed')
			versn=os.path.join(bakpath,Thisver)
			stdin1,stdout1,stderr1=Ssh.Exe_cmd('/usr/bin/cp -rfv %s %s' %(srcpath,versn))
			if len(stderr1.read()) != 0:
				raise SystemExit(stderr1.read())
			Diff_file_list=self.Diff.Ssh_dffoflist(srcpath,versn)
			if len(Diff_file_list) == 0:
				print ("-------------------备份成功! version=%s------------" %versn)
			else:
				raise SystemExit('-------------------备份失败，文件不同-------------------------\n',Diff_file_list)
		except Exception,e:
			print e
		finally:
			Ssh.Close_conn()