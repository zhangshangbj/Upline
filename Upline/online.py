#! /bin/python
#-*- coding: utf-8 -*-


from Upline.ctversion import version
from Upline.backup import bkproject
from Upline.checkfile import dffile
from Upline.cpfiles import cpfiles
import os
import sys

__metaclass__=type
class toline:
	def __init__(self):
		pass
		
	def toline(self,srcdir,distdir,srccodename,projectname,bkpath,flag):
		'''
		上线操作
		:param srcdir: 新代码目录
		:param distdir: 工程目录
		:param projectname: 工程名
		:return:
		'''
		adver=version()
		#工程上线版本号
		ver=adver.mkversion(distdir,projectname)
		#备份工程
		bkpject=bkproject()
		bkpj=bkpject.backup(distdir,projectname,bkpath,'1')
		#对比工程文件验证备份是否完整
		dfpj=dffile()
		pjsrcdir=os.path.join(distdir,projectname)
		dflist=dfpj.dffoflist(pjsrcdir,bkpj)
		if len(dflist)==0:
			flagback='Project backup to bkpath success!'
			print flagback
			bk_status1=1
		else:
			flagback="Project backup failed,Shut Off this action!"
			print "diffirent files"
			print dflist
			bk_status1=0
			return ver,flagback,bk_status1,dflist,{},[],7
		#复制代码到工程目录
		toli=cpfiles()
		sfile,dfile,allfile=toli.cpfiles(srcdir,distdir,srccodename,projectname)
		#校验上线文件
		check=dffile()
		sname=os.path.join(srcdir,srccodename)
		dname=os.path.join(distdir,projectname)
		dictcheck=check.dffofdict(sname,dname)
		if len(dictcheck) == 0:
			flag2back='check the code coverd success!'
			bk_status2=1
		else:
			flag2back='Code coverd failed'
			bk_status2=0
		return ver,flagback,bk_status1,dflist,dictcheck,allfile,flag2back,bk_status2