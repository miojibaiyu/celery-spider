#! /usr/bin/env python
#coding=utf-8

from __future__ import absolute_import
from myapp.celery import app
from myapp.common import get_proxy
from myapp.util.Browser import MechanizeCrawler as MC
from myapp.spider_paser import __crawler as paser
from myapp.logger import logger 
import sys
import json
import urllib
import urllib2
import cookielib
from lxml import html as HTML
import os
import time
import traceback

user_agent_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36']

class urllibCrawler(object):
    def __init__(self):
	self.httpHandler = urllib2.HTTPHandler(debuglevel=0)
	self.httpsHandler = urllib2.HTTPSHandler(debuglevel=0)
	self.cookie = cookielib.CookieJar()
	self.debug = True
	self.header = {}
	self.p = ''
	self.refer = {}
	
    def set_debug(self,flag = False):
	if flag:
	    self.httpHandler = urllib2.HTTPHandler(debuglevel=1)
	    self.httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
	
    def add_header(self,dict):
	self.header = dict
    def add_referer(self,refer):
	self.refer = refer

    def keep_cookie(self, flag = True):
	self.cookie = True
	
    def set_proxy(self,p):
	self.proxy = p
    
    def req(self, method, url_base, paras = {}, paras_type = 1, html_flag = False, time_out = 60):
        if method.lower() == 'get':
            url = url_base + urllib.urlencode(paras)
        elif method.lower() == 'post':
            url = url_base
        else:
            logger.error('req, wrong method(post or get)')
            sys.exit(-1)

        html = ''
        try:
	    request= urllib2.Request(url)
            request.add_headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0')]
	    if self.header != {}:
	    	for key,value in self.header.items():
	    	    request.add_header(key,value)
	    self.header = {}
	    if self.p != '':
	    	request.set_proxy(self.p,'http')
	    	request.set_proxy(self.p,'https')
	    if self.refer != {}:
	    	for key,value in self.refer.items():
	    	    request.add_header(key,value)
	    self.refer = {}

	    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie), self.httpHandler)
	    urllib2.install_opener(opener)
            if method.lower() == 'get':
		resp = urllib2.urlopen(request, timeout = time_out)
               # resp = self.br.open(url, timeout=time_out)
            else:
                if paras_type == 1:
                    paras = json.dumps(paras)
                elif paras_type == 0:
                    paras = urllib.urlencode(paras)
                elif paras_type == 2:
                    pass
                else:
                    logger.error('req, wrong paras type( 0 or 1)')
                #resp = self.br.open(url, paras, timeout=time_out)
		#安装opener,此后调用urlopen()时都会使用安装过的opener对象

		resp = opener.open(request, paras)
            if html_flag:
		html=resp.read()
        
        except Exception, e:
            if self.debug:
                logger.error(traceback.format_exc(e))
        return html


class download(object):
    def __init__(self):
	self.temp = paser()
	self.objmc = {}
	self.objreq = {}

    def load_by_request(self, spi, url, name):
	refer = spi['refer']
	mode = spi['mode']
	spi_url = spi['spi_url']
	post_type = spi['post_type']
	post_data = spi['post_data']
	isproxy = spi['isproxy']
	debug = spi['debug']

	p = get_proxy('XXXX')
	if not p:
	    logger.error('get proxy error ... %s',str(p))
		
	key = name.split('__')[0]
	if self.objreq.has_key(key):
	    req = self.objreq[key]
	else:	
	    req = urllibCrawler()
	    self.objreq[key]=req

	req.set_debug(debug)
	if isproxy != '' and p:
	    req.set_proxy(isproxy)
	if refer != '':
	    req.add_referer(self.refer)
	if spi_url != '':
	    req.req( self.mode, self.spi_url)
	try:
	    if mode == 'post':
		page = req.req( mode, post_url, paras = post_data ,paras_type =  post_type, html_flag = True)
	    else:
	  	page = req.req( mode, url, html_flag = True)
	except Exception, e:
	    #traceback.print_exc(e)
	    logger.error('loading by urllib :: %s',traceback.format_exc(e))
	
	return page ,p

    def load_by_mc(self, spi, url, name):	
	refer = spi['refer']
	mode = spi['mode']
	spi_url = spi['spi_url']
	post_type = spi['post_type']
	post_data = spi['post_data']
	post_url  = spi['post_url']
	isproxy = spi['isproxy']
	debug = spi['debug']
		
	key = name.split('__')[0]
	if self.objmc.has_key(key):
	    mc = self.objmc[key]
	else:	
	    mc = MC()
	    mc.set_debug(debug)
	    self.objmc[key]=mc
	
	if isproxy != '': 
	    p = get_proxy(source = 'citytraffic')
	    if not p:
	    	logger.error('get proxy error ... %s',str(p))
	    else:
	    	logger.info('this proxy is ... %s',str(p))
	    	mc.set_proxy(p)
	if refer != '':
	    mc.add_referer(self.refer)
	if spi_url != '':
	    mc.req( self.mode, self.spi_url)

	try:
	    if mode == 'post':
		page = mc.req( mode, post_url, paras = post_data ,paras_type =  post_type, html_flag = True)
	    else:
	  	page = mc.req( mode, url, html_flag = True)
	except Exception, e:
	    #traceback.print_exc(e)
	    logger.error('load by mc ...<-!error::%s!-> <-!proxy::%s!->',traceback.format_exc(e),str(p))
	
	return page,p



if __name__ == '__main__':
	spi = {'mode':'get',\
		'refer':'',\
		'way':'mc',\
		'spi_url':'',\
		'post_url':'',\
		'post_data':'',\
		'post_type':0,\
		'coding':'utf8',\
		'isproxy':'',\
		'debug':'False'\
		}
	url = 'http://www.baidu.com/'
	filename = 'a'
	download().load_by_request(spi,url,filename)
