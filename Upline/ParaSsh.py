#! /usr/bin/python
#-*- coding:utf-8 -*-

'''
使用ssh登录执行命令
使用sftp传输文件
'''
try:

	import os
	import sys
	import paramiko
except ImportError:
	print 'Please install the packege of paramiko'
	sys.exit(1)

class ParmSsh(object):
	def __init__(self,hostname='127.0.0.1',username='carry'):
		'''
		ssh连接目标主机
		'''
		self.sftphost=(hostname,22)
		self.ssh=paramiko.SSHClient()
		self.sftp=paramiko.Transport(self.sftphost)
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
		self.privatekey = os.path.expanduser('/home/carry/.ssh/id_rsa')
		self.key=paramiko.RSAKey.from_private_key_file(self.privatekey)

		self.ssh.connect(hostname=hostname,username=username,pkey=self.key,timeout=300)
		self.sftp.connect(username=username,pkey=self.key)
	def Exe_cmd(self,Cmd):
		stdin,stdout,stderr=self.ssh.exec_command(Cmd)
		return stdin,stdout,stderr

	def Trans_File(self,Action,Dist,Src=''):
		'''

		:param Action: get:sftp下载 put：sftp上传 mkdir：目标机器创建目录 rmdir：目标机器删除目录
		:param Dist:
		:param Src:
		:return:
		'''
		try:
			Trans=paramiko.SFTPClient.from_transport(self.sftp)
			if Action == 'get':
				Trans.get(Dist,Src)
			if Action == 'put':
				Trans.put(Src,Dist)
			if Action == 'mkdir':
				Trans.mkdir(Dist)
			if Action == 'rmdir':
				Trans.rmdir(Dist)
		except Exception,e:
			print e

	def Close_conn(self):
		self.ssh.close()
		self.sftp.close()





