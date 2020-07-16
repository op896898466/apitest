from django.test import TestCase

# Create your tests here.
import sys


import os

taskinfo = os.popen('netstat -ano | findstr 8028')

line = taskinfo.readline()

aList = line.split()

taskinfo.close()
if aList:
    pid = aList[4]
    os.popen('taskkill /pid %s /f' % pid)

print("win" in sys.platform)