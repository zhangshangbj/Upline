#! /bin/python
#-*- coding: utf-8 -*-

'''
回滚操作
'''


from Upline.backup import bkproject
from Upline.ctversion import version
from Upline.cpfiles import cpfiles
import os

class rollback:
	def __init__(self,hostname='127.0.0.1',username='carry'):
		self.hostname=hostname
		self.username=username
		self.sfiles=[]
		self.dfiles=[]
		self.allfiles=[]

	def rollback(self,projectname,bakpath,projectpath,flag):
		'''
		回滚可用的备份工程
		'''
		cpfile=cpfiles()
		cver=version()
		backup=bkproject()
		vrsn=cver.chover(projectname,bakpath)
		backup.backup(projectpath,projectname,bakpath,flag)
		bkpath=os.path.join(bakpath,projectname,vrsn)
		srcpath=os.path.join(projectpath,projectname)
		self.sfiles,self.dfiles,self.allfiles=cpfile.cpfiles(bkpath,srcpath)
		return self.sfiles,self.dfiles,self.allfiles

	def Ssh_rollback(self,hostname,username, projectname, bakpath, projectpath,flag):

		'''
		:param projectname:
		:param bakpath:
		:param projectpath:
		:return:
		'''

		cpfile = cpfiles()
		cver = version()
		backup = bkproject()
		vrsn = cver.Ssh_chover(projectname, bakpath)
		backup.Ssh_backup(hostname,username,projectpath, projectname, bakpath,flag)
		bkpath = os.path.join(bakpath, projectname, vrsn)
		srcpath = os.path.join(projectpath, projectname)
		self.sfiles, self.dfiles, self.allfiles = cpfile.Ssh_cpfiles(bkpath, srcpath)