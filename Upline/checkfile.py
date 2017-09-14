#! /bin/python
#-*- coding: utf-8 -*-

import re
from Upline import getmd5
from Upline.ParaSsh import ParmSsh

__metaclass__=type
class dffile(object):
	'''
	使用md5串儿来对比文件是否一样
	'''
	def __init__(self):
		self.different=[]
		self.dictdf={}
		self.dictdd={}
		self.src={}
		self.dist={}
		self.Src_list=[]
		self.Dist_list=[]
		self.Src_key_md5={}
		self.Dist_key_md5={}
		
	def dffoflist(self,srcpath,distpath):
		'''
		对比文件返回一个列表
		:param srcpath: 1目录（字符串）
		:param distpath: 2目录（字符串）
		:return: 两个目录文件差异列表
		'''
		md1=getmd5()
		md2=getmd5()
		self.src=md1.Get_Md5_Of_Files(srcpath)
		self.dist=md2.Get_Md5_Of_Files(distpath)
		for key in self.src.keys():
			try:
				if self.src[key] == self.dist[key]:
					continue
				self.different.append(key)
			except KeyError:
				self.different.append(key)
		return self.different

	def dffofdict(self,srcpath,distpath):
		'''
		对比文件返回一个字典
		:param srcpath: 1目录
		:param distpath: 2目录
		:return: 两个目录文件差异字典
		'''
		md1=getmd5()
		md2=getmd5()
		self.src=md1.Get_Md5_Of_Files(srcpath)
		self.dist=md2.Get_Md5_Of_Files(distpath)
		index=1
		for key in self.src.keys():
			try:
				if self.src[key] == self.dist[key]:
					continue
				self.dictdf[str(index)]=key
			except KeyError:
				self.dictdf[str(index)]=key
			index+=1
		return self.dictdf	 	

	def Ssh_dffoflist(self,hostname,username,srcpath,distpath):
		'''
		对比文件返回一个列表
		:param srcpath: 1目录（字符串）
		:param distpath: 2目录（字符串）
		:return: 两个目录文件差异列表
		'''
		Ssh = ParmSsh(hostname, username)
		try:
			stdin,stdout,stderr=Ssh.Exe_cmd('cd %s ; find ./* | grep -v lost+found' %(srcpath))
			Src_files=stdout.readlines()[:]
			for i in Src_files:
				stdin1,stdout1,stderr1=Ssh.Exe_cmd('md5sum %s' %(i))
				self.Src_list.append(stdout1.read().split('\t'))
			stdin,stdout,stderr=Ssh.Exe_cmd('cd %s ; find ./* | grep -v lost+found' %(distpath))
			Dist_files=stdout.readlines()
			for k in Dist_files:
				stdin2,stdout2,stderr2=Ssh.Exe_cmd('md5sum %s' %(k))
				self.Dist_list.append(stdout2.read().split('\t'))
			for j in self.Dist_list:
				self.Src_key_md5[re.sub('^%s' %(srcpath),'',j[1].replace('^.*/'))]=j[0]
			for k in self.Dist_list:
				self.Dist_key_md5[re.sub('^%s' %(distpath),'',k[1].replace('^.*/'))]=k[0]
			index=1
			for key in self.Src_key_md5.keys():
				if self.Src_key_md5[key] != self.Dist_key_md5[key]:
					self.different.append(self.Src_key_md5[key])
				index+=1
			return self.different
		except Exception,e:
			print e
		finally:
			self.Ssh.Close_conn()

	def Ssh_diffoffiles(self,hostname,username,srcfiles,distfiles,srcdir,distdir):
		'''
		对比指定列表内的文件
		:param srcpath: 1文件列表1（列表）
		:param distpath: 2文件列表2（列表）
		:return: 两个目录文件差异列表
		'''
		Ssh = ParmSsh(hostname, username)
		try:
			for i in srcfiles:
				stdin1, stdout1, stderr1 = Ssh.Exe_cmd("md5sum %s | awk '{print $1}'" % (i))
				self.src[i.replace(srcdir,'')]=stdout1.read()
			for k in distfiles:
				stdin2, stdout2, stderr2 = Ssh.Exe_cmd("md5sum %s | awk '{print $1}'" % (k))
				self.dist[re.sub('^.*%s$' %(distdir),distdir,k)]=stdout2.read()
			for key in self.src.keys():
				try:
					if self.src[key] == self.dist[key]:
						continue
					self.different.append(key)
				except KeyError:
					self.different.append(key)
			return self.different
		except Exception,e:
			print e
		finally:
			self.Ssh.Close_conn()