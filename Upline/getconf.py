#! /bin/python
# -*- coding: utf-8 -*-
'''
配置文件相关！
'''

import ConfigParser
import json

__metaclass__ = type


class getconf:
    '''
	获取配置文件信息返回一个列表
	'''

    def __init__(self):
        self.confdict = {}
        self.name=[]

    def get(self, projectname):
        config = ConfigParser.ConfigParser()
        with open("/etc/Upline/%s.conf" %(projectname), "r") as cfgfile:
            config.readfp(cfgfile)
            self.name = config.options(projectname)
            for indexname in self.name:
                self.confdict[indexname] = config.get(projectname, indexname)
        return self.confdict


class showconf(getconf):
    def __init__(self):
        getconf.__init__(self)
        self.diction = ''
        self.diction1 = ''

    def showconf(self, projectname):
        """
		显示项目配置文件
		"""
        self.diction = self.get(projectname)
        self.diction1 = json.dumps(self.diction, indent=1)
        print self.diction1
