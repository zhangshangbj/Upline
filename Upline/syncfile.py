#! /bin/python
#-*- coding: utf-8 -*-

from commands import getoutput
from Upline.strformt import strformt
import os




__metaclass__=type
class syncfile:
	def __init__(self):
		self.a=''
		self.b=''
		self.strft=strformt()
		self.fl=[]

	def fullsync(self,syncip,projectname,srcdir,syncflag,excptfile):
		srdir=os.path.join(srcdir,projectname)
		self.fl=excptfile.split(',')
		ecfile=self.strft.strarg(self.fl)
		self.a=getoutput('rsync '+syncflag+' '+ecfile+' '+syncip+'::'+projectname+' '+srdir)
		return self.a
				
	def partofsync(self,syncip,projectname,srcdir,filelist,syncflag,excptfile):
		self.fl = excptfile.split(',')
		ecfile = self.strft.strarg(self.fl)
		for i in filelist:
			self.a=self.a+getoutput('rsync '+syncflag+' '+ecfile+syncip+'::'+projectname+i+' '+os.path.join(srcdir,i))
			self.b=self.b+self.a
		return self.b