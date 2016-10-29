#!/usr/bin/env python
#-*- coding:utf-8 -*-


from __future__ import absolute_import
from kombu import Queue,Exchange
from datetime import timedelta
 
CELERY_TASK_RESULT_EXPIRES=3600
CELERY_TASK_SERIALIZER='json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_RESULT_SERIALIZER='json'
#CELERYD_CONCURRENCY = 50  #worker 的并发数量
#CELERYD_PREFETCH_MULTIPLIER = 4 # celery worker 每次去rabbitmq取任务的数量
#CELERYD_MAX_TASKS_PER_CHILD = 40 # 每个worker执行了多少任务就会死掉
#CELERY_DEFAULT_QUEUE = "default_dongwm" # 默认的队列，如果一个消息不符合其他的队列就会放在默认队列里面

CELERY_DEFAULT_EXCHANGE = 'agent'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
 
CELERT_QUEUES =  (
  Queue('machine1',exchange='agent',routing_key='machine1'),
 # Queue('machine2',exchange='agent',routing_key='machine2'),
)








