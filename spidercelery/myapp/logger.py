#!/usr/bin/env python
#coding=UTF8
'''
    @author: ybai
    @time: 2015-07-12
    @desc:

'''
import logging
import logging.config

#用字典保存日志级别
format_dict = {
   1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   2 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
   5 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
}



#开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件   
class Logger():
    def __init__(self, logfile):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''

        # 创建一个logger
        self.logger = logging.getLogger('commontraffic')
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        #ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        #self.logger.addHandler(ch)

    
    def getlog(self):
        return self.logger
'''
#配置日志
FORMAT = "%(asctime)-15s %(threadName)s %(filename)s:%(lineno)d %(levelname)s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

logger = logging.getLogger('insertLog')
logger.setLevel(logging.NOTSET)
'''

logger  =  Logger('log').getlog()

if __name__ == '__main__':
	logger  =  Logger().getlog()

	logger.info('afdsfasf')







