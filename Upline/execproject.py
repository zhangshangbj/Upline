#! /bin/python
#-*- coding: utf-8 -*-

'''
这个文件是用来表示执行的action，现在分为启动，停止，重启，3个动作
其中启动分为两类，一类为tomcat，一类为通用工程
'''


import os
import commands
from psutil import Popen
from subprocess import PIPE
from subprocess import Popen as popen
from Upline import fullrmdir
from Upline.ParaSsh import ParmSsh

__metaclass__=type
class execpj:
	def __init__(self):
		self.execarg=[]
		self.Bin_path =''

	def tstart(self,pjpath,pjexecfile):
		'''
		tomcat启动方法，需要删除缓存文件夹	
		'''		
		self.tcache=os.path.join(pjpath,'work/Catalina')
		if os.path.isdir(self.tcache):
			fullrmdir(self.tcache)
			path=os.path.join(pjpath,'bin',pjexecfile)
			self.execarg.append(path)
			self.execarg.append('start')
			p=Popen(self.execarg,stdout=PIPE)
			p.communicate()
		return p.communicate()
	def mstart(self,pjpath,pjexecfile):
		'''
		通用启动方法
		:param pjpath:
		:param pjexecfile:
		:return:
		'''

		path=os.path.join(pjpath,'bin',pjexecfile)
		self.execarg=self.execarg.append(path)
		self.execarg=self.execarg.append('start')
		p=Popen(self.execarg,stdout=PIPE)
		p.communicate()
		return p.communicate()
	def pstart(self,pjpath,pjexecfile):
		'''
		provider启动方法
		'''			
		listpid=popen("ps x | grep -v grep | grep "+pjpath+" | awk '{print $1}'",shell=True,stdout=PIPE,stderr=PIPE).stdout.readlines()
		if len(listpid) != 0:
			raise ("The Project is running!")
		path=os.path.join(pjpath,'bin',pjexecfile)
		self.pidpath=os.path.join(pjpath,'logs/.run.pid')
		self.execarg.append(path)
		self.execarg.append('start')
		p=Popen(self.execarg,stdout=PIPE)
		p.name()
		return p.communicate()
			
	def stop(self,pjpath,type1):
		'''
		停止工程，直接使用kill -9
		'''
		if type1 == 'provider':
			pjpath = pjpath.replace('/bin', '')

		listpid=popen("ps x | grep -v grep | grep "+pjpath+" | awk '{print $1}'",shell=True,stdout=PIPE,stderr=PIPE).stdout.readlines()
		for pid in listpid:
			p=p+commands.getoutput("kill -9 "+pid)
		return p.communicate()

	def restart(self,pjpath,pjexecfile,type1):
		sp = self.stop(pjpath,type1)
		if type1 == 'tomcat':
			st=self.tstart(pjpath,pjexecfile)
		if type1 == 'provider':
			st=self.pstart(pjpath,pjexecfile)
		if type1 == 'common':
			st=self.mstart(pjpath,pjexecfile)
		return sp,st


	def Ssh_tstart(self,hostname,username,Exe_path):
		'''
		tomcat启动方法，需要删除缓存文件夹
		'''
		Ssh = ParmSsh(hostname, username)
		try:
			self.tcache = os.path.join(Exe_path, 'work/Catalina')
			self.Bin_path=os.path.join(Exe_path,'/bin/startup.sh')
			Ssh.Exe_cmd('rm -rf %s' %(self.tcache))
			stdin,stdout,stderr=Ssh.Exe_cmd('sh $s start' %(self.Bin_path))
			if len(stderr.read()) == 0:
				Ssh.Close_conn()
				return stdout.read()
			else:
				Ssh.Close_conn()
				raise IOError(stderr.read())
		except Exception,e:
			print e
		finally:
			Ssh.Close_conn()

	def Ssh_mstart(self,hostname,username, pjpath, pjexecfile):
		'''
		通用启动方法
		:param pjpath:
		:param pjexecfile:
		:return:
		'''
		Ssh = ParmSsh(hostname, username)
		try:
			self.Bin_path = os.path.join(pjpath, 'bin', pjexecfile)
			stdin,stdout,stderr=Ssh.Exe_cmd('sh $s start' %(self.Bin_path))
			if len(stderr.read()) == 0:
				Ssh.Close_conn()
				return stdout.read()
			else:
				Ssh.Close_conn()
				raise IOError(stderr.read())
		except Exception,e:
			print e
		finally:
			Ssh.Close_conn()

	def Ssh_pstart(self,hostname,username, pjpath):
		'''
		provider启动方法
		'''
		Ssh = ParmSsh(hostname, username)
		try:
			Exe_path = os.path.join(pjpath, 'bin','server.sh')
			Pid_path = os.path.join(pjpath, 'logs/.run.pid')
			stdin1, stdout1, stderr1 = Ssh.Exe_cmd("ps x | grep -v grep | grep %s  | awk '{print $1}'" %(pjpath))
			if len(stdout1.readlines()) != 0:
				Ssh.Close_conn()
				raise ("The Project is running!")
			stdin2, stdout2, stderr2 = Ssh.Exe_cmd('ls %s ' %(Pid_path))
			if len(stderr2.read()) == 0:
				Ssh.Close_conn()
				raise ("The Pid file is exist")
			stdin3, stdout3, stderr3 = Ssh.Exe_cmd=('sh %s start' %(Exe_path))
			if len(stderr3.read()) != 0:
				Ssh.Close_conn()
				raise (stderr3.read())
		except Exception,e:
			print e
		finally:
			Ssh.Close_conn()

	def Ssh_stop(self,hostname,username, pjpath, type1):
		'''
		停止工程，直接使用kill -9
		'''
		Ssh = ParmSsh(hostname, username)
		try:
			if type1 == 'provider':
				pjpath = pjpath.replace('/bin', '')
			stdin, stdout, stderr = Ssh.Exe_cmd("ps x | grep -v grep | grep %s  | awk '{print $1}'" % (pjpath))
			for pid in stdout.readlines():
				Ssh.Exe_cmd("kill -9 %s" %(pid))
			Ssh.Close_conn()
		except Exception,e:
			print e
		finally:
			Ssh.Close_conn()

	def Ssh_restart(self,hostname,username, pjpath, type1, pjexecfile=''):
		sp = self.Ssh_stop(pjpath, type1)
		if type1 == 'tomcat':
			st = self.Ssh_tstart(hostname,username,pjpath)
		if type1 == 'provider':
			st = self.Ssh_pstart(hostname,username,pjpath)
		if type1 == 'common':
			st = self.Ssh_mstart(hostname,username,pjpath, pjexecfile)
		return sp, st