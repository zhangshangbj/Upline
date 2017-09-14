#! /bin/python
#-*- coding: utf-8 -*-

__metaclass__=type
class strformt:
	def __init__(self):
		self.a=''
		self.b=[]
		self.strarg=' --exclude '
		pass
							
	def tostr(self,arg):
		if type(arg) == type(self.a):
			return arg
		if type(arg) == type(self.b):
			l=len(self.b)
			if len(l) == 0:
				self.strarg=''
			b=1
			for i in arg :
				try:
					self.strarg=self.strarg+' '+ '\"'+str(i)+'\" '
					if b != l:
						self.strarg=self.strarg+' --exclude '
				except TypeError:
					print 'Type Error , '+str(type(i))+'can not to str!'
					pass
		return self.strarg