#coding=utf-8
__author__ = 'Carry lee'
import logging

def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Started')
    logging.info('Doing something')
    logging.info('Finished')

if __name__ == '__main__':
    main()