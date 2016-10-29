#! /usr/bin/env python
#coding=utf-8


import sys
import json
import re
import os
#import Queue
import time
import csv
import traceback
from myapp.logger import logger
#from spider_tree import Tree
#from pymongo import MongoClient


def md5(string):
    import hashlib
    m = hashlib.md5()   
    m.update(string)
    return m.hexdigest()


class task_scheduling(object):
    
    def __init__(self, queue, resq_timeout = 30):
	self.__resq_timeout = resq_timeout
	self.__dict = {}
	self.cra_d = open('data3','w')
	self.__name_dict = {}
	self._cqs = queue._cqs
	self._cqx = queue._cqx
	#self.tree = Tree() 
	self.fail = open('failtask','w')
	#self.thread_handle()

    def __del__(self):
	self.fail.close()
	self.cra_d.close()
	logger.info('process running down ...')
	'''
	lname:线路名，sname:站名，type:类型，realtime:running时间，spacetime:间隔时间，coordinates:坐标
	'''

    def thread_handle(self):		
	logger.info('...thread_handle start...')
	while True:
	    
	    try:
		res = self._cqx.get(True, self.__resq_timeout)
	    except Exception ,e:
		'''队列开始空了'''
		logger.info('result queue cqx is empty')
	    else:
		#logger.info('running task')
		try:
			ged = res.get(timeout = 1)
		except:
			try:
				self._cqx.put(res)
			except:
				logger.error('time out task put cqx again error ...')
		else:
			self.res_handle(ged)

    def res_handle(self,result):
	    request = result['task']['oldinfo']
	    task = result['task']
	    data = result['data']
	    logger.info('flag is '+str(result['flag']))
	    if result['flag'] :
	    	self.product_pooltask(task)
	    	self.process_data(data)
	    	#self.keep_file(html)
	    	#self.keep_mongo(html)
	    else:
		self.process_fail(request)
	
    def process_fail(self, failtask):
	print failtask
	print os.getcwd()
	self.fail.write(str(failtask)+'\n')
	self.fail.flush()
	del  failtask

    def process_data(self, pooldata):
	nlst = pooldata['filename'].split('/')[1].split('__')
	path = []
	k=''
	for n in nlst:
	    if k != n:
		k = n
	   	path.append(k)
	empty = ['filename']
	for key in pooldata:
	    if pooldata[key] == []:
		empty.append(key)
	for key in empty:
	    del pooldata[key]

	tmp = '&&'.join(path)+'###'+str(pooldata)+'\n'
	logger.info('write line to data3')
	self.cra_d.write(tmp)
	self.cra_d.flush()

    def product_pooltask(self,poolres):
	pooltask= poolres
	spi_lst = pooltask['spi_act']
	exp_lst = pooltask['exp_act']
	oldinfo = pooltask['oldinfo']
	newinfo = pooltask['newinfo']	
	
	file_new = []
	for file in newinfo:
	    on = oldinfo[1]
	    n = file[1]
	    if self.__name_dict.has_key(on+n):
		self.__name_dict[on+n] += 1
	    else:
		self.__name_dict[on+n]  = 0
	    if self.__name_dict[on+n] != 0:
		n = n+'_'+str(self.__name_dict[on+n])

	    newurl = file[0]
	    oldurl = oldinfo[0]
	    nus = newurl.split('/')
	    if 'http' in newurl:
		pass
	    elif nus[0] == '..':
	    	for fl in nus:
		    if fl == '..':
		    	nus=nus[1:]#remove('..')
		    	oldurl = '/'.join(oldurl.split('/')[:-2])+'/'
	    	    else:
		    	break
	    	newurl = oldurl+'/'.join(nus)
	    else:
		oldurl = '/'.join(oldurl.split('/')[:-1])+'/'
		if nus[0] == '.':
		    newurl = oldurl+'/'.join(nus[1:])
		else:
		    newurl = oldurl+'/'.join(nus)
	    if oldinfo == []:
		file_new.append([newurl,n,file[2]])	
	    else:
	    	file_new.append([newurl,oldinfo[1]+'__'+n,file[2]])
	    
	for info in file_new:
	    if info[2] == -1:
		continue
	    newtask = {}
	    newtask['info'] = info
	    if type(info[0]) == type(()):
	    	for i in range(len(info[0])):
		    spi_lst[info[2]]['post_data'].replace('miaoji@'+str(i),info[0][i])
	    newtask['spi_act'] = spi_lst
	    newtask['exp_act'] = exp_lst
	    try:
	    	self._cqs.put(newtask)
	    except Exception, e:
	    	logger.error('(file:%s)requestqueue...%s',__name__,traceback.format_exc(e))

	
    def keep_file(self,poolhtml):
	data = poolhtml['filedata']
	path = poolhtml['filename']
	md5path = path.split('/')[0]+'/'+md5(path.split('/')[1])
	with open(md5path,'w') as f:
	    f.write(data)

    def keep_mongo(self,poolhtml):
	data = poolhtml['filedata']
	path = poolhtml['filename']
	key = path.split('/')[1]
	conn = MongoClient('localhost', 27017)
	db = conn.admin
	db.authenticate("baiyu","123")
	db.user.save({'key':key,'value':data})
	#content = db.user.find()



