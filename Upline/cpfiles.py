#! /bin/python
#-*- coding: utf-8 -*-

'''
覆盖文件到指定目录
'''

from subprocess import Popen
from subprocess import PIPE
from Upline.ParaSsh import ParmSsh
import os

__metaclass__=type
class cpfiles:
	def __init__(self):
		self.distfile=[]
		self.srcfile=[]
		self.bkstr=[]
		self.liststr=[]

	def cpfiles(self,src,dist):
		'''
		从原目录将文件覆盖到指定目录,并返回 源文件列表，目标文件列表，源文件、目标文件对应列表
		:param src: 补丁包目录（和目标工程目录的目录树需要一致）
		:param dist: 目标工程目录
		:return: srcfile：拷贝的源文件列表；distfile：拷贝的目标文件列表；bkstr：拷贝的所有文件对应列表
		'''

		if os.path.isdir(dist):
			pass
		else:
			os.mkdir(dist)
		self.liststr=Popen('/usr/bin/cp -rfv '+src+'/* '+dist+'/',shell=True,stdout=PIPE,stderr=PIPE).stdout.readlines()
		for key in self.liststr:
			a=key.replace('\n','').replace('\"','').split('->')
			self.bkstr.append(key.replace('\"',''))
			self.srcfile.append(a[0])
			self.distfile.append(a[1])
		return self.srcfile,self.distfile,self.bkstr

	def Ssh_cpfiles(self,hostname,username,src,dist):
		'''
		从原目录将文件覆盖到指定目录,并返回 源文件列表，目标文件列表，源文件、目标文件对应列表
		:param src: 补丁包目录（和目标工程目录的目录树需要一致）
		:param dist: 目标工程目录
		:return: srcfile：拷贝的源文件列表；distfile：拷贝的目标文件列表；bkstr：拷贝的所有文件对应列表
		'''

		Ssh = ParmSsh(hostname, username)
		Popen('cd %s' %(src),shell=True,stdout=PIPE,stderr=PIPE)
		Popen('tar -cvzf /tmp/packege.tar.gz ./*',shell=True,stdout=PIPE,stderr=PIPE)
		Ssh.Trans_File('put','/tmp/packege.tar.gz','/tmp/packege.tar.gz')
		try:
			Ssh.Exe_cmd('mkdir /tmp/Packege')
		except OSError:
			pass
		Ssh.Exe_cmd('tar -xvzf /tmp/packege.tar.gz -C /tmp/Packege/')
		stdin,stdout,stderr=Ssh.Exe_cmd('/usr/bin/cp -rfv /tmp/Packege/* %s/' %(dist))
		for key in stdout.readlines():
			a=key.replace('\n','').replace('\"','').split('->')
			self.bkstr.append(key.replace('\"',''))
			self.srcfile.append(a[0])
			self.distfile.append(a[1])
		return self.srcfile,self.distfile,self.bkstr