#! /usr/bin/python
#-*- coding:utf-8 -*_

import os
from Upline.ctversion import version
from Upline.cpfiles import cpfiles
from subprocess import Popen
from subprocess import PIPE

class Packege(object):
	def __init__(self,flag='1'):
		'''

		:param flag: 1表示上线之前几个一起合并的版本，0表示只上线指定版本，其他版本不做变更
		'''
		self.Ver=version()
		self.cp=cpfiles()
		self.flag=flag

	def Tag_packege(self,Pkg_path,Projectname,flag):
		'''

		:param Pkg_path: 包目录
		:param Projectname: 工程名
		:param flag: 版本号
		:param This_ver：生成的版本号
		:param Real_path：操作目录
		:param Version_path：操作目录下的version目录
		:param verlist：Version_path目录下文件列表
		:param New_code：存放新代码目录
		:param Buffer_path：多次上线集合目录
		:param version：Real_path下生成的版本号
		:param srcver：Version_path下已版本号命名的代码目录
		:return:上线的路径，版本号
		'''
		This_ver=self.Ver.mkversion(Pkg_path,Projectname,flag,'1')
		Real_path = os.path.join(Pkg_path, Projectname)
		if not os.path.isdir(Real_path):
			os.mkdir(Real_path)
		Version_path = os.path.join(Real_path,'version')
		if not os.path.isdir(Version_path):
			os.mkdir(Version_path)
		New_code=os.path.join(Real_path,'Newcode')
		verlist=os.listdir(Version_path).sort(reverse=True)
		Buffer_path = os.path.join(Real_path, 'srccode')
		if not os.path.isdir(Buffer_path):
			os.mkdir(Buffer_path)
		version = os.path.join(Buffer_path, 'version')
		try:
			if This_ver <= verlist[0]:
				print "版本号小于上次的版本号"
				raise ('Err')
		except Exception:
			pass
		srcver=os.path.join(Version_path,This_ver)
		if not os.path.join(srcver):
			os.mkdir(srcver)
		os.mkdir(Version_path)
		self.cp.cpfiles(New_code,Version_path)
		self.cp.cpfiles(Version_path,os.path.join(Real_path,'Buffer'))
		Popen("touch %s/version" % (srcver),shell=True,stdout=PIPE,stderr=PIPE)
		Popen("sed -i '1i\%s' %s/version" % (This_ver, version),shell=True,stdout=PIPE,stderr=PIPE)
		if self.flag=='1':
			self.cp.cpfiles('%s/version'%(Real_path), version)
			return os.path.join(Real_path,'Buffer'),This_ver
		elif self.flag=='0':
			Popen("touch %s/version" % (srcver), shell=True, stdout=PIPE, stderr=PIPE)
			Popen("sed -i '1i\%s' %s/version" % (This_ver, version), shell=True, stdout=PIPE, stderr=PIPE)
			return srcver,This_ver,

