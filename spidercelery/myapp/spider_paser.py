#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
	@author:baiyu
	@date: 2015-07-16
	@desc: crawl and parse ...
'''

import re
import urllib2
import traceback 
from lxml import html as HTML
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import HTMLParser

def decodeHtml(input):
    h = HTMLParser.HTMLParser()
    s = h.unescape(input)
    return s

week = ['mon','tue','wed','thu','fri','sat','sun']
class __crawler:
	def __init__(self):
		self.count = 0
		print 'init,explian'
	    
	def temp1(self,page):
		result = []
		self.count += 1
		dom = HTML.fromstring(page)
		root = dom.find_class('lowBg14')[0]
		
		two = root.find_class('lowBgFFF')
		for one in two:
			try:
				ur=one.xpath('./span/a/@href')[0]
			except:
				continue
			url = 'http://ekikara.jp/newdata/'+ur[3:]
			name=one.xpath('./span/a/text()')[0]
			result.append([url,name,1])
			
		return result
	def temp2(self,page):
		result = []
		self.count += 1
		dom = HTML.fromstring(page)
		
		root = dom.xpath('//*[@valign="bottom"]')[1]
		root = root.xpath('./table/tbody/tr/td/a')
		for r in root:
			url = r.xpath('./@href')[0]
			nm  = r.xpath('./img/@alt')[0]
			result.append([url,nm,2])
		result+=self.temp5(page)
		'''
		假日url
		'''
		return result
	def temp3(self,page):
		result = []
		self.count += 1
		dom = HTML.fromstring(page)
		root = dom.find_class('lowBg14')[0].xpath('./table/tbody/tr[5]')[0]
		many = root.xpath('./td')[1:]
		#many = root.find_class('lowBgFFF')
		name = 'detail'
		for one in many:
			url=one.xpath('./span/a/@href')[0]
			result.append([url,name,4])
		'''详情URL'''
		return result

	def temp4(self,page):
		result = []
		self.count += 1
		dom = HTML.fromstring(page)
		try:
    			root = dom.find_class('lowBg01')[0].xpath('./table/tbody/tr')
			root[1].xpath('./td[2]/span/text()')[0]
		except:
			root = dom.find_class('lowBg01')[1].xpath('./table/tbody/tr')
			
		infos = root[:6]
		table = root[8:-1]
		d = {}
		for row in infos:
		    k = row.xpath('./td[1]/span/span/text()')[0].strip()
		    #v = row.xpath('./td[2]/span/text()')[0].strip()
    		    v = row.xpath('./td[2]/span')[0].text_content().strip().replace(' ','')
		    d[k]=v
		s=[]
		for row in table:
    		    name=row.xpath('./td[1]')[0].text_content().strip()
		    time=row.xpath('./td[2]')[0].text_content().strip()
		    zt=row.xpath('./td[3]')[0].text_content().strip()
		    s.append(name+'$$'+time+'$$'+zt)
		info = json.dumps(d)
		return [info+'$$$'+'||'.join(s)]
	def temp5(self,page):
		result = []
		self.count += 1
		dom = HTML.fromstring(page)
		
		root = dom.xpath('//*[@name="page"]/option/@value')
		filename='pgs'
		for url in root:
			result.append([url+'.htm',filename,3])
		'''
		分页url
		'''
		return result

	def temp6(self,page):
		result = []
		self.count += 1
		dom = HTML.fromstring(page)
	
		root = dom.find_class('lowBg01')[0].xpath('./table[1]/tbody[1]/tr/td[1]')[1:]
		sl = map(lambda x:x.xpath('./span')[0].text_content().strip(),root)
		info = '$$'.join(sl)
		return [info]
	def temp7(self,page):
		result = []
		self.count += 1
		dom = HTML.fromstring(page)
		root = dom.find_class('lowBg14')[0].xpath('./table/tbody/tr')
		line_name = root[0].xpath('./td[1]/span[1]/span[1]/text()')
		train_no = '$$'.join(root[1].xpath('./td/span[1]/span[1]/text()'))
		train_name = map(lambda x:x.xpath('./span[1]/text()')[0]+'$'+x.xpath('./span[2]/text()')[0],root[2].xpath('./td')[1:])
		train_name = '列車名$$'+'$$'.join(train_name)
		runday = '$$'.join(root[3].xpath('./td/span[1]/span[1]/text()'))
		
		pre = map(lambda x:x.xpath('./span[1]')[0].text_content(),root[5].xpath('./td')[1:])
		pre = root[5].xpath('./td')[0].xpath('./span[1]/span[1]/text()')[0]+'$$'+'$$'.join(pre)
		tables=[]
		for rot in root[6:-1]:

			table = map(lambda x:'$'.join(x.xpath('./span/text()')),rot.xpath('./td')[2:])
			table = '$$'.join(table)
			#print table
			fa =[]
			for i in rot.xpath('./td')[1].xpath('./span[1]/span'):
				try:
					fa.append(i.xpath('./a/text()')[0])
				except IndexError,e:
					fa.append(i.xpath('./text()')[0])

			fa = '$'.join(fa)
			azh = rot.xpath('./td')[0].xpath('./span[1]/span[1]')[0]
			azh = HTML.tostring(azh)
			az=[]
			for a in azh.split('<br>'):
				try:
					b= re.findall(r'>(.*)<',a)[0].encode('utf8')
				except:
					b=a.strip()
				az.append(decodeHtml(b))
			az = '$'.join(az[:-1])
			table = az+'$$'+fa+'$$'+table
			tables.append(table)
		ntable = []

		for i in range(len(tables[0].split('$$'))):
			nn = []
			for ntab in tables:
				nn.append(ntab.split('$$')[i])
			ntable.append('$'.join(nn))

		tables = '$$'.join(ntable)
		#tables = '####'.join(tables)
		next = map(lambda x:x.xpath('./span[1]')[0].text_content(),root[-1].xpath('./td')[1:])
		next = root[-1].xpath('./td')[0].xpath('./span[1]/span[1]/text()')[0]+'$$'+'$$'.join(next)


		d = {}
		d['line_name']=line_name
		d['train_no']=train_no
		d['train_name']=train_name
		d['runday']=runday
		d['pre']=pre
		d['table']=tables
		d['next']=next
		info = json.dumps(d)
		return [info]

	def temp8(self,page):
		result = []
		self.count += 1
		dom = HTML.fromstring(page)
	
		root = dom.find_class('lowBg14')[0].xpath('./table/tbody/tr')

		azh = root[6].xpath('./td')[0].xpath('./span[1]/span[1]/a/text()')
		year = '2016'
		month='03'
		day = '01'
		hour = '12'
		mins = '01'
		urls = []
		for i in range(len(azh)):
			for j in range(i+1,len(azh)):
				dept,dest = azh[i],azh[j]
				tmp = 'http://www.jorudan.co.jp/norikae/cgi/nori.cgi?Sok=%E6%B1%BA+%E5%AE%9A&eki1='+dept+'&eok1=R-&eki2='+dest+'&eok2=R-&eki3=&eok3=&eki4=&eok4=&eki5=&eok5=&eki6=&eok6=&rf=nr&pg=0&Dym='+year+month+'&Ddd='+day+'&Dhh='+hour+'&Dmn='+mins+'&Cway=0&C1=0&C2=0&C3=0&C4=0&C6=2&Cmap1=&Cfp=1&Czu=2'
				urls.append(dept+'_'+dest+'$$'+tmp)
		urls = '###'.join(urls)
		return [urls]
if __name__ == '__main__':
    task = ''
