#coding=utf8
import urllib
import mechanize
import cookielib
import logging as log
import json
log.basicConfig(level=log.INFO)

user_agent_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1;     WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36']

class MechanizeCrawler(object):

    #init
    def __init__(self, referer='', headers={}, p=''):
        log.info('MechanizeCrawler init start')
        self.debug = False
        self.br = mechanize.Browser()
        self.respons = ''

        #Cookie Jar
        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)

        #Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.p = p
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0')]

        #Follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), \
                max_time=1)

        #add headers, referer can also be put here
        for k, v in headers.items():
            self.br.addheaders += [(k,v)]

        #set proxy
        if p:
            self.br.set_proxies({'http': p})
        
        log.info('MechanizeCrawler init done!')

    #Want debugging messages?
    def set_debug(self, flag= False):
        log.info('MechanizeCrawler.set_debug start')
        self.br.set_debug_http(flag)
        self.br.set_handle_redirect(flag)
        self.br.set_debug_responses(flag)
        log.info('MechanizeCrawler.set_debug done!')

    #the req fun crawl web via get, post, put method
    def req(self, method, url, paras={}, paras_type=1, html_flag=False, time_out=60):

        try:
            html = ''
            error = ''
            if method.lower() == 'get':
                url = url + urllib.urlencode(paras) #just for Compatible
            if method.lower() == 'post':
                if paras_type == 1: #type 1, json.dumps
                    paras = json.dumps(paras)
                elif paras_type == 0: #type 0, urllib.urlencode
                    paras = urllib.urlencode(paras)
                elif paras_type == 2: #type 2 unchanged
                    pass
                self.respons = self.br.open(url, paras, timeout=time_out)
                log.info('MechanizeCrawler.req.post done!')

            elif method.lower() == 'get':
                self.respons = self.br.open(url, timeout=time_out)
                log.info('MechanizeCrawler.req.get done!')

            elif method.lower() == 'put':
                self.respons = self.br.open(PutRequest(url, paras))
            else:
                log.error('MechanizeCrawler.req error unkonwn method!')
            if html_flag:
                html = self.respons.get_data()
        except Exception, e:
            error = 'Crawl Error With Proxy'
        return html, error

    def set_proxy(self, p):
        self.br.set_proxies({'http':p})
    def get_url_of_response(self):
        return self.br.geturl()

    def get_cookie_str(self):
        t = []
        for e in self.cj:
           t.append(e.name+'='+e.value)
        return ';'.join(t)

    def add_cookie(self,cookie_str): # "sid=abcdef; expires=Wednesday, 09-Nov-06 23:12:40 GMT"
        self.br.set_cookie(cookie_str)

    def get_response(self):
        return self.br.response()

    def add_referer(self, url):
        d = dict(self.br.addheaders)
        d['Referer'] = url
        self.br.addheaders = d.items()
    def add_header(self, headers={}):
        d = dict(self.br.addheaders)
        for k in headers:
            d[k] = headers[k]
            self.br.addheaders = d.items()

    def get_cookie_handle(self):
        cookie_handle_pos = -1
        for i in xrange(0, len(self.br.handlers)):
            #logger.info(mc.br.handlers[i])
            if str(self.br.handlers[i]).find('Cookie') != -1: 
                cookie_handle_pos = i 
        if cookie_handle_pos != -1: 
            return self.br.handlers[cookie_handle_pos]
        else:
            return None 

    def get_cookie(self, method, url_base, paras = {}, paras_type = 1, time_out = 60):
        if method.lower() == 'get':
            url = url_base + urllib.urlencode(paras)
        elif method.lower() == 'post':
            url = url_base
        else:
            pass
        cookie = None
        error = ''

        try:
            if method.lower() == 'get':
                resp = self.br.open(url, timeout=time_out)

            else:
                if paras_type == 1:
                    paras = json.dumps(paras)
                elif paras_type == 0:
                    paras = urllib.urlencode(paras)
                elif paras_type == 2:
                    pass
                else:
                    pass

                resp = self.br.open(url, paras, timeout=time_out)
                    
            cookie = self.cj._cookies
        except Exception, e:
            print str(e)
            error = 'Crawl Error With Proxy'
            print error

        return cookie, error

    def get_url(self, method, url_base, paras = {}, paras_type = 1, time_out = 60):

        if method.lower() == 'get':
            url = url_base + urllib.urlencode(paras)
        elif method.lower() == 'post':
            url = url_base
        else:
            sys.exit(-1)

        getURL = ''
        error = ''
        try:
            if method.lower() == 'get':
                resp = self.br.open(url, timeout=time_out)
            else:
                if paras_type == 1:
                    paras = json.dumps(paras)
                elif paras_type == 0:
                    paras = urllib.urlencode(paras)
                elif paras_type == 2:
                    pass
                else:
                    logger.error('req, wrong paras type( 0 or 1)')
                resp = self.br.open(url, paras, timeout=time_out)

            getURL = self.br.geturl()
        except Exception, e:
            error = str(e)
            error = 'Crawl Error With Proxy'
            if self.debug:
                logger.error(str(e))
        self.resp = resp

        return getURL, error 


class PutRequest(mechanize.Request):
    def get_method(self):
        return 'PUT'


if __name__ == '__main__':
    mc = MechanizeCrawler()
    mc.set_debug(True)


    mc.add_referer('http:www.baidu.com')
    mc.add_header({
        'a':1,
        'b':2,
        'c':3,
        'Content-Type':'application/json'
        })

    page, _ = mc.req('get', 'http://www.mioji.com', html_flag=1)
    raise
    h = mc.get_cookie_handle()
    print h.CookieJar
    raise
    mc.add_cookie('miaoji=zhangyang')
    print mc.get_cookie_str(), '%%%%%%%%'
    mc.add_cookie('miao=xiaohong')
    print mc.get_cookie_str(), '%%%%%%%%%'

    mc.req('get', 'http://www.mioji.com')
    mc.req('get', 'http://www.baidu.com')
    print mc.get_url()
    print mc.get_cookie_str()
