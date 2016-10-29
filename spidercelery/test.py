#!/usr/bin/env python
#-*- coding:utf-8 -*-

import traceback 
from spider_schedule import  task_scheduling
from myapp.spider_static import spi
from myapp.agent import paser_page
from myapp.agent import add
from myapp.logger import logger
import os
import csv
from multiprocessing import Process,Queue
class myqueue(object):
    def __init__(self):
	self._cqs = Queue()
	self._cqx = Queue()


class etask (object):
	def __init__(self,info):

		spi['mode']='get'
		spi['way']='req'
		spi['isproxy']='GG'
		spi['debug']=False

		exp1 = {'url_res':'temp.temp1(page)','realtime':'temp.temp6(page)'}#上行，下行url，日文格式站名
		exp2 = {'url_res':'temp.temp2(page)'}#周末，节假日URL 及 详情URL	
		exp3 = {'url_res':'temp.temp5(page)'}#分页URL
		exp4 = {'url_res':'temp.temp3(page)','spacetime':'temp.temp7(page)'}#详情URL,时间表
		exp5 = {'sname':'temp.temp4(page)'}#详细信息
		self.task = {}
		self.task['info'] = info
		self.task['exp_act'] = [exp1,exp2,exp3,exp4,exp5]
		self.task['spi_act'] = [spi,spi,spi,spi,spi]
	def get_task(self):
		return self.task
	def __del__(self):
		del self.task

def mkcitydir(self,city_name):
	city_name = city_name
	if not os.path.exists(city_name):
		os.mkdir(city_name)
'''
lname:线路名，sname:站名，type:类型，realtime:running时间，spacetime:间隔时间，coordinates:坐标
'''

def init_task(mq,link):
	lines = csv.reader(file(link,'rb'))
	nd = {}
	cd = {}
	for line in lines:
		url = line[-1]
		if not cd.has_key(url):
			cd[url]=0
		else:
			continue
		filename = 'japan'+'/'+line[2]
		if not nd.has_key(filename):
			nd[filename]=0
		else:
			nd[filename]+=1
			filename = filename+'_'+str(nd[filename])
		task=etask([url,filename,0]).get_task()
		mq._cqs.put(task)
	
	while 1:
	    	try:
			task = mq._cqs.get(True, 10)
	    	except Exception ,e:
			logger.info('...get cqs task out of time...')
		else:
			logger.info('...run a task...')
			result = paser_page.apply_async(args=[task],queue='machine1',routing_key='machine1')
			#result = result.get()
			#print result
			try:
				mq._cqx.put(result)
			except Exception ,e:
				logger.error('...put cqx result error...')
def start_celery(link):
	mq = myqueue()
	ts = task_scheduling(mq)
	process_list = []
	p = Process(target=init_task,args=(mq,link,))
	process_list.append(p)
	p = Process(target=ts.thread_handle,args=())
	process_list.append(p)

	for j in process_list:
		j.start()
	for j in process_list:
		j.join()


if __name__ == '__main__':
	start_celery('link.csv')
	#add.apply_async(args=[123,353],queue='machine1',routing_key='machine1')


