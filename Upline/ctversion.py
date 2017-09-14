#! /bin/python
#-*- coding: utf-8 -*-


import os
import json
import time
import sys
from fnmatch import filter
from Upline.ParaSsh import ParmSsh

__metaclass__=type
class version:
	'''
	程序的版本控制
	'''
	def __init__(self):
		self.dicver=''
		self.dictversion={}
		self.verdic={}
		self.path=''

	def mkversion(self,srcpath,projectname,flag1,flag2='0'):
		'''
		再工程目录下追加一个版本号
		:param srcpath: 工程目录
		:param projectname: 工程名
		:param flag1: 版本号
		:param flag2： ‘1’不在工程内写入版本号，‘0’在工程内写入版本号
		:return: 返回版本信息
		'''
		dateofnow = str(time.strftime('%Y.%m.%d.%H.%M.%S', time.localtime(time.time())))
		pjversion=os.path.join(srcpath,projectname,'version')
		if not os.path.isfile(pjversion):
			os.mknod(pjversion)
		else:
			with open(pjversion,'r') as oldver:
				oldver.seek(0)
				Oversion=oldver.readline()

		cver = ("%s_version.%s_%s\n" % (projectname, flag1, dateofnow))
		if flag2 == '1':
			pass
		elif flag2 == '0':
			try :
				if cver >= Oversion:
					with open(pjversion,'r+') as ver:
						old=ver.read()
						ver.seek(0)
						ver.write(cver)
						ver.write(old)
				else:
					print "Your version is too small! The version mast >= lastest version"
					return 'Err'
			except NameError:
				with open(pjversion, 'r+') as ver:
					old = ver.read()
					ver.seek(0)
					ver.write(cver)
					ver.write(old)
		else:
			print 'Flag Errer '
			sys.exit(1)
		return cver.replace('\n', '')
	def listbkver(self,bakpath,projectname):
		'''
		列出备份目录下的版本，并返回一个字典
		:param bakpath: 备份目录（例如:/bak/gatewayweb/）
		:param projectname: 工程名（例如：gatewayweb）
		:return: verdic 返回一个字典
		'''
		try:
			self.listver=filter(os.listdir(bakpath),'%s_version.*'%(projectname))
			self.listver.sort(reverse=True)
			self.findex=1
			for i in self.listver[0:10]:
				self.verdic[self.findex]=i
				self.findex+=1
		except TypeError:
			return self.listver
		self.jsonver=json.dumps(self.verdic, indent=1)
		print self.jsonver
		return self.verdic
				
	def chover(self,bakpath,projectname):
		'''
		选择一个版本
		:param bakpath: 备份目录路径（例如:/bak/gatewayweb/）
		:return:
		'''
		self.verdic=self.listbkver(bakpath,projectname)
		keywords=raw_input("Please input a num in 1-10 to select a version:")
		try:
			if len(keywords)==0:
				chokey='1'
			elif int(keywords)>10:
				print 'Out of range!'
				sys.exit(1)
			else:
				chokey=keywords
		except TypeError:
			chokey = '1'
		vrsn = self.verdic[int(chokey)]
		return vrsn

	def lastver(self,bakpath,projectname):
		"""
		选择一个最后的版本
		"""
		self.verdic=self.listbkver(bakpath,projectname)
		vrsn=self.verdic[1]
		return vrsn

	def Ssh_mkversion(self,hostname, username,srcpath,projectname,flag1,flag2='0'):
		'''
		再工程目录下追加一个版本号
		:param srcpath: 工程目录
		:param projectname: 工程名
		:param flag1: 版本号
		:param flag2： ‘1’不在工程内写入版本号，‘0’在工程内写入版本号
		:return: 返回版本信息
		'''
		Ssh = ParmSsh(hostname, username)
		try:

			dateofnow = str(time.strftime('%Y.%m.%d.%H.%M.%S', time.localtime(time.time())))
			pjversion=os.path.join(srcpath,projectname,'version')
			Ssh.Exe_cmd('touch %s' %(pjversion))

			cver = ("%s_version.%s_%s\n" % (projectname, flag1, dateofnow))
			if flag2 == '1':
				pass
			elif flag2 == '0':
				stdin1, stdout1, stderr = Ssh.Exe_cmd('sed -n 1p %s' % (pjversion))
				Oversion = stdout1.read()
				if cver >= Oversion:
					Ssh.Exe_cmd("sed -i '1i\%s' %s" % (cver, pjversion))
				else:
					print "版本号小于上次的版本号"
					return 'Err'
			else:
				raise SystemExit('Flag Errer!')
			return cver.replace('\n', '')
		except Exception,e:
			print e
		finally:
			Ssh.Close_conn()
	def Ssh_listbkver(self,hostname, username,bakpath,projectname):
		'''
		列出备份目录下的版本，并返回一个字典
		:param bakpath: 备份目录（例如:/bak/gatewayweb/）
		:param projectname: 工程名（例如：gatewayweb）
		:return: verdic 返回一个字典
		'''
		Ssh = ParmSsh(hostname, username)
		try:
			try:
				stdin1,stdout1,stderr1=Ssh.Exe_cmd('ls %s/ | grep %s_version.* | tac' %(bakpath,projectname))

				self.findex=1
				for i in stdout1.readlines()[0:10]:
					self.verdic[self.findex]=i
					self.findex+=1
			except TypeError:
				return stdout1.readlines()
			self.jsonver=json.dumps(self.verdic, indent=1)
			print self.jsonver
			return self.verdic

		except Exception,e:
			print e
		finally:
			Ssh.Close_conn()

	def Ssh_chover(self,bakpath,projectname):
		'''
		选择一个版本
		:param bakpath: 备份目录路径（例如:/bak/gatewayweb/）
		:return:
		'''
		self.verdic=self.Ssh_listbkver(bakpath,projectname)
		keywords=raw_input("输出1-10选择一个版本: ")
		try:
			if len(keywords)==0:
				chokey='1'
			elif int(keywords)>10:
				print 'Out of range!'
				sys.exit(1)
			else:
				chokey=keywords
		except TypeError:
			chokey = '1'
		vrsn = self.verdic[int(chokey)]
		return vrsn

	def Ssh_lastver(self,bakpath,projectname):
		"""
		选择一个最后的版本
		"""
		self.verdic=self.Ssh_listbkver(bakpath,projectname)
		vrsn=self.verdic[1]
		return vrsn