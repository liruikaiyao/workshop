#coding=utf-8
__author__ = 'Carry lee'
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)

logging.debug('I am world')
logging.error('you are loser')
logging.info({'a':'b'})