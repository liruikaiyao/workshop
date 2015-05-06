#coding=utf-8

import sys
import os
import subprocess

python_path = 'python '
file_path = os.path.realpath(__file__).replace(os.path.basename(__file__),'')+'../'+sys.argv[1]+'/'
script = sys.argv[2]
print script

#os.system(python_path+file_path+script+'.py')
subprocess.call(python_path+file_path+script+'.py')