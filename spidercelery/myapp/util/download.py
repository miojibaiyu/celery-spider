#!/usr/bin/env python
#coding=GBK
'''
    Created on 2011-5-5
    @author: devingong
    @desc:
        ������ҳ��ͼƬ
        ������ҳ��1. ����gzip/deflateѹ������ҳ��2. ʶ����ҳ�ı��룬��ͳһת��Ϊָ���ı���
'''
import socket
import urllib2
import httplib
import urlparse
import time
import StringIO
import gzip
import sys
import random


#set default timeout
socket.setdefaulttimeout( 30 )
#user-agent
#encoding

def get_page(url, retry=3, interval=0.5, proxy = None):
    '''
        ����ָ��URL����ҳ��retryΪ���Դ�����intervalΪ���Լ��ʱ��
    '''
    t = 0
    while t < retry:
        if t > 1:
            proxy = None 
        fd = None
        try:
            request = urllib2.Request(url)
            request.add_header('Accept-encoding', 'gzip')
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22')
            if proxy != None:
                request.set_proxy(proxy, "http")
            opener = urllib2.build_opener()
            
            fd = opener.open(request)
            if fd != None:
                if 'text/html' not in fd.headers.get("Content-Type") and \
                    "text/xml" not in fd.headers.get("Content-Type") and \
                    "text/css" not in fd.headers.get("Content-Type")  :
                    return None
                
                contentEncoding = fd.headers.get("Content-Encoding")
                data = None
                if contentEncoding != None and 'gzip' in contentEncoding:
                    compresseddata = fd.read()
                    compressedstream = StringIO.StringIO(compresseddata)  
                    gzipper = gzip.GzipFile(fileobj=compressedstream)
                    data = gzipper.read()
                else:
                    data = fd.read()

                return data
        except Exception, e:
            print >> sys.stderr, "download %s by proxy %s error: %s" %(url, proxy,str(e)) 
            if hasattr(e,'code') and e.code == 404:      #��ҳ������
                return None
            t += 1
            time.sleep(interval * t)
            
        if fd != None:  fd.close()
        
    return None

def get_image(url, retry = 3, interval = 0.5):
    '''
        ����ָ��URL��ͼƬ��retryΪ���Դ�����intervalΪ���Լ��ʱ��
    '''
    imgData = None
    t = 0
    while t < retry:
        fd = None
        try:
            fd = urllib.urlopen(url)
            if fd != None:
                imgData = fd.read()

                return imgData
        except Exception, e:
            logger.error("download %s error: %s" %(url,str(e)) )
            t += 1
            time.sleep(interval * t)  
              
        if fd != None:  fd.close()

    return imgData
        
    
