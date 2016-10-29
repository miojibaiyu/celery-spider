#!/usr/bin/env python
#-*- coding:utf-8 -*-

from __future__ import absolute_import
from myapp.celery import app
from myapp.logger import logger
from myapp.spider_down import download

from myapp.common import get_proxy
from myapp.util.Browser import MechanizeCrawler as MC

import traceback
import os

MAX=10
Islocal=False

@app.task
def add(x,y):
    return {'the value is ':str(x+y)}
 
@app.task
def getline(url):
    mc = MC()
    p = get_proxy('XXXX')
    if not p:
	logger.error('get proxy error ... %s',str(p))
		
    mc.set_proxy(p)
    page = mc.req( 'get', url, html_flag = True)
    return page
 
 
@app.task
def paser_page( kwds):
	
	realtime = []
	spacetime = []
	lname = []
	sname = []
	type = []
	url_res = []
	coordinates = []
	dl = download()
	task = kwds
	key_l = {
		'lname':[],\
		'sname':[],\
		'type':[],\
		'coordinates':[],\
		'realtime':[],\
		'spacetime':[],\
		'url_res':[]\
		}

	task_url = task['info'][0]	
	path     = task['info'][1]	
	filename = path.split('/')[0]+'/'+md5(path.split('/')[1])
	city_name = path.split('/')[0]
	step     = task['info'][2]	
	exp_act  = task['exp_act'][step]
	spi_act  = task['spi_act'][step]
	temp = dl.temp
	count = 0
	flag  = True
	p = '0.0.0.0:0'
	for key, value in exp_act.items():
	    if count == 0:
		i = 0
		while key_l[key] == []:
		    i += 1
		    if i > MAX:
	    		logger.info('a task fail ::%s',str(task['info']))
			flag = False
			break
		    try:
		    	if os.path.exists(filename) and Islocal:
		    	    with open(filename,'r') as file :	
			    	page = file.read()
			else:
		    	    if spi_act['way'].lower() == 'req':
		            	page,p = dl.load_by_request(spi_act,task_url,filename)
		    	    elif spi_act['way'].lower() == 'mc':
		            	page,p = dl.load_by_mc(spi_act,task_url,filename)
		        exec(key+'='+value)
		    except Exception, e:
	    		logger.error('a error spider :: <-!error::%s!-> <-!task::%s!-> <-!proxy::%s!->',traceback.format_exc(e),str(task['info']),str(p))
		    else:
		    	logger.info('task success :: <-!task::%s!-> <-!proxy::%s!->',str(task['info']),str(p))

		    if key == 'lname':
		    	key_l[key] = lname
		    elif key == 'sname':
			key_l[key] = sname
		    elif key == 'type':
			key_l[key] = type
		    elif key == 'spacetime':
			key_l[key] = spacetime
		    elif key == 'realtime':
			key_l[key] = realtime
		    elif key == 'coordinates':
			key_l[key] = coordinates
		    elif key == 'url_res':
			key_l[key] = url_res
	    else:
		if i >= MAX:
		    break
		try:
		    exec(key+'='+value)
		except Exception, e:
	    	    logger.error('not first validate error :: <-!error::%s!-> <-!task::%s!->',traceback.format_exc(e),str(task['info']))
	    count += 1
	if flag:
	    mkcitydir(city_name)
	    with open(filename,'w') as file :	
		page = file.write(page)
		
	res = {}
	res['flag'] = flag
	res['data'] = {}
	res['task'] = {}
	#res['html'] = {}
	#res['html']['filename'] = path
	#res['html']['filedata'] = page
	res['data']['filename'] = path
	res['data']['sname']    = sname
	res['data']['type']     = type
	res['data']['spacetime']= spacetime
	res['data']['realtime'] = realtime
	res['data']['coordinates']     = coordinates
	res['task']['spi_act']  = task['spi_act'] 
	res['task']['exp_act']  = task['exp_act']
	res['task']['oldinfo']  = task['info']
	res['task']['newinfo']  = url_res
	
	return res

 
def getlength(stri):
    return len(stri)

def mkcitydir(city_name):
	city_name = city_name
	if not os.path.exists(city_name):
		os.mkdir(city_name)

def md5(string):
    import hashlib
    m = hashlib.md5()   
    m.update(string)
    return m.hexdigest()

