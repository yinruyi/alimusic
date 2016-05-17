# -*- coding: utf-8 -*-
import os
import sys
import string
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')
abspath = os.getcwd()


def readTxt(path):
    with open(path,'r') as file:
        for line in file:
            line = line.replace('\n','')
            temp = line.split(',')
            print temp


if __name__=='__main__':
    readTxt('H:\\dataset\\alimusic\\mars_tianchi_user_actions.csv')