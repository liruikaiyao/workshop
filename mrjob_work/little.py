# coding=utf-8
__author__ = 'Carry lee'
import sys


for elem in sys.stdin:
    legs = elem.split('/')
    print '\t'.join(legs[:2])
