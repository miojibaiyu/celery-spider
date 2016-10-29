#!/usr/bin/env python
#coding=UTF-8
'''
    Created on 2014-03-22
    @author: devin
    @desc:
        
'''
#import jsonlib
import time
from util import http_client

proxy_client = http_client.HttpClientPool("10.136.8.94:8086")
#proxy_client2 = http_client.HttpClientPool("10.136.11.134:8087")
proxy_client2 = http_client.HttpClientPool("120.132.92.44:8086")

def set_proxy_client(client):
    global proxy_client
    proxy_client = client

#def get_proxy(source = None, allow_ports = [], forbid_ports = [], allow_regions = [], forbid_regions = [], user = 'crawler', passwd = 'spider@miaoji!', proxy_info = {}):
#def get_proxy(source = None, allow_ports = [], forbid_ports = [], allow_regions = [], forbid_regions = [], user = 'platform', passwd = 'platformmioji', proxy_info = {}):
def get_proxy(source = None, allow_ports = [], forbid_ports = [], allow_regions = [], forbid_regions = [], user = 'overall', passwd = 'oproxyverall', proxy_info = {}):
    if proxy_info == {}:
        pass
    else:
        # todo, 当前全部使用默认值
        if proxy_info.has_key("allow_ports"):
            allow_ports = proxy_info['allow_ports']
        if proxy_info.has_key("forbid_ports"):
            forbid_ports = proxy_info['forbid_ports']
        if proxy_info.has_key("allow_regions"):
            allow_regions = proxy_info['allow_regions']
        if proxy_info.has_key("forbid_regions"):
            forbid_regions = proxy_info['forbid_regions']

    allow = ""
    forbid = ""
    allow_regions_str = ""
    forbid_regions_str = ""

    if len(allow_ports) != 0:
        allow = '_'.join( [str(i) for i in allow_ports] ) 
    if len(forbid_ports) != 0:
        forbid = '_'.join( [str(i) for i in forbid_ports] )

    if len(allow_regions) != 0:
        allow_regions_str = '_'.join( [i for i in allow_regions] )
    if len(forbid_regions) != 0:
        forbid_regions_str = '_'.join( [i for i in forbid_regions] )
    
    try:
        p = proxy_client2.get("/proxy?source=%s&user=overall&passwd=oproxyverall" % source)
    except:
        p = ''

    return p

def invalid_proxy(proxy,source):
    return
    #if proxy != None:
    #    proxy_client.get("/update_proxy?status=Invalid&p=%s&source=%s"%(proxy,source))


def update_proxy(source_name, proxy, start_time, error_code):
    speed = time.time() - start_time
    if proxy != None or proxy != 'NULL':
        proxy_client2.get('/update_proxy?source=%s&proxy=%s&error=%s&speed=%s' % (source_name, proxy, \
                str(error_code), str(speed)))

    return None


if __name__ == '__main__':
    p = get_proxy(forbid_regions=['CN'])
    print p
