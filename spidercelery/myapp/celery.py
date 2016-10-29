#!/usr/bin/env python
#-*- coding:utf-8 -*-


from __future__ import absolute_import
from celery import Celery
app = Celery('myapp',
             broker='amqp://guest@10.10.180.145//',
             backend='amqp://guest@10.10.180.145//',
             include=['myapp.agent'])
 
app.config_from_object('myapp.config')
 
if __name__ == '__main__':
  app.start()



