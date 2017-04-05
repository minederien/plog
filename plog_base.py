print("############ Log Parser 0.9 ############")
sfnames = ['CaseMI3a.200.syslog.ioserver.dat',  'syslog.IOServer.CaseMI3X.dat',  'CaseMI_modbus_issue.csv']
sfnames = ['CaseMI_modbus_issue3.csv',  'CaseMI_modbus_issue4.csv',  'CaseMI_modbus_issue2.csv']
sfnames = ['/home/thomasr/code/python/iodlog/CaseMI_modbus_issue-10lines.csv']
sfname = "/home/thomasr/code/python/iodlog/CaseMI_modbus_issue2.csv"
sfname = "L3lab.small01.syslog.IOServer.Clust01.PLC_IOS_p.dat"
#sfname = "CaseMI_modbus_issue-10lines.csv"
import re
import time
import statistics
import sys
import os
from stat import * # ST_SIZE etc
import platform
#import string 
sPlat = platform.system()
print('var sPlat = {}, lowered = {}' .format(sPlat,str.lower(sPlat)))
if str.lower(sPlat) == 'windows' :
    sLogFolder = "logs\\"
elif str.lower(sPlat) == 'linux' :
    sLogFolder = "logs\/"
sFullFname = sLogFolder + sfname
print('Running on ',sPlat)
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
ticks1 = time.time()
# First of all, make sure the file is viable and can be opened
try:
    h1=open(sFullFname,  'r', errors='ignore')
    print('h1 = ', str(h1))
    st = os.stat(sFullFname)
except IOError as e:
    errno, strerror = e.args
    print("I/O error({0}): {1}".format(errno,strerror))
    print('kann Datei nicht öffnen:', sFullFname)
    sys.exit(1)
else:
    print('file size: {} bytes' .format(st[ST_SIZE]))
    print("file modified:", time.asctime(time.localtime(st[ST_MTIME])))
# regex:  '.*(\d+).*\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)'
# regex from RegexBuddy:  r".*(\d+).*\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)"
# rgx = re.compile(r'.*(\d+).*\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b).*(\bQuery|Response\b).*')
sPatt='asdl'
sFtype = 'CSV'
sFtype = 'syslog'

#rgx = re.compile(r'\"(\d+)\".*?([0-9]+\.?[0-9]+).*?\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b).*?\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b).*Trans:\s*(\d+)')
if sFtype == 'CSV':
    rgx = re.compile(r'\"(\d+)\".*?(?P<time>[0-9]+\.?[0-9]+).*? \
\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b).*?\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b) \
.+\s*(Query|Response):\s+Trans:\s+(?P<transno>\d+)')
elif sFtype == 'syslog' :
    rgx=re.compile(r"(?P<date>[\d-]+)\s(?P<time>[\d:\.]+)\s.*DRIVERTRACE.*(?P<qtype>CTDRV_READ|CTDRV_STATUS_UNIT)(?P<lereste>.*)")
else :
    rgx= re.compile(r'.*(\d+).*\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)')
print('Opening log file ' + sFullFname)
try :
    h1=open(sFullFname,  'r', errors='ignore')
    # print('Handle is '+str(h1))
    iCnt=0
    iDrd=0
    iMiss=0
    iTran=0
    fTime1=0.0
    fTime2=0.0
    fTranTime=0.0
    fMean = 0.0
    fStDev = 0.0 
    mList=[]
    mListAll=[]
    mTime=[]
    mListDrvRd = [] #driver read queries
    sM1 = ''
    for sline in h1 :
        iCnt=iCnt+1
        mymatch = rgx.match(sline)
        if mymatch :
            if sFtype == 'CSV' :
                iDrd+=1
                if iTran!=int(mymatch.group('transno')) :
                    iTran = int(mymatch.group('transno'))
                    fTime1= float(mymatch.group('time'))
                else :
                    fTime2 = float(mymatch.group('time'))
                    fTranTime = (fTime2 - fTime1)*1000.0
                    mList = [iTran, fTime1, fTime2, fTranTime]
                    mListAll.append(mList) 
            elif sFtype == 'syslog' :
                sM1 = mymatch.group('qtype')
                #print('query type = {}' .format(sM1))
                if sM1 == 'CTDRV_READ' :
                    mListDrvRd.append(mymatch)
                    iDrd+=1
                else :
                    print('no syslog qtype match')
                    mList=[mymatch.group(1), mymatch.group(2),mymatch.group(3),mymatch.group(4)]
                    mListAll.append(mList) 
            else :
                 mList=[mymatch.group(1),mymatch.group(2),mymatch.group(3),mymatch.group(4),mymatch.group(5)]
        else :
            #print('¡Nada por aca!')
            iMiss+=1
    if sFtype == 'CSV' :
        for wsLine in mListAll :
            sPrint = '' 
            mTime.append(wsLine[3])
            for wsItem in wsLine :
                sPrint = sPrint + str(wsItem) + '--'
            print(sPrint)
        print('matched {} lines out of {} ' .format(iDrd,iCnt))
        print('list size = ' + str(len(mListAll)))
        print('query/response exchanges captured = ' + str(len(mTime)))
        fMean = statistics.mean(mTime)
        print('ave response time = ' + str(fMean))
        fStDev = statistics.stdev(mTime)
        print('std dev = ' + str(fStDev))
        ii = 0
        #ii2 = 0
        for fRTime in mTime :
            if fRTime - fMean > fStDev :
                ii += 1
                #print('long response = {} ms' .format(fRTime))
        print('excessive times = ' + str(ii))
    elif sFtype == 'syslog' :
        print('Abgestimmt {} Zeilen von {} ' .format(iDrd,iCnt))
        print('list DrvRd size = ' + str(len(mListDrvRd)))
        print('list Rest size = ' + str(len(mListAll)))
    ticks2 = time.time()
    print('this run took {} ms' .format((ticks2-ticks1)*1000))
except:
    print('echec! --  ' + sfname)
