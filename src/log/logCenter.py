# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 14:20:59 2020

@author: wangyouqish
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler
def getLogger(name):
    os.chdir(os.path.join(os.path.abspath(".."),'log'))
    logger = logging.getLogger(name)
    if(logger.handlers==[]):
        logger.setLevel(level = logging.INFO)
        #handler = logging.FileHandler(name+".txt")
        handler = TimedRotatingFileHandler(filename=name+".txt", when="D", interval=3, backupCount=3)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        logger.addHandler(handler)
        logger.addHandler(console)#日志平台+文件输出
    return logger

def destroyLogger(logger):
    logger.handlers=[]
