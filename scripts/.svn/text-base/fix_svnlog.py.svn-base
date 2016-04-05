#!/usr/bin/python

import os
import sys
from subprocess import Popen,STDOUT,PIPE
import glob
import re

dir_svnlog='/home/django/lvnproject/Weblvn/my_media/svnhistory'
file_tocheck='/home/django/head.txt'
pattern='\d{6}'

with open(file_tocheck,'r+') as f:

    
    if not re.search(pattern,f.readline()):
        print 'ERROR:head.txt has no revision written in it'
        os.chdir(dir_svnlog)
        x = glob.glob('*.txt')
        new=[int(i.strip('.txt')) for i in x]
        last_revision = sorted(new)[-1]
        print 'I will write '+last_revision+' to head.txt now'
        os.chdir('/home/django/')
        f.seek(0)
        f.write(str(last_revision))

        print 'Execute poll.sh'
        cmd='./poll.sh'
        p = Popen(cmd,shell=True,stdout=PIPE,stderr=STDOUT)
        p.communicate()


    else:
        f.seek(0)
        print 'head.txt has revision in it: ',f.readline()
        
        


