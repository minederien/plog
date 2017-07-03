''' Demarche:
1. Get file name and type
2. File object - vet the file
3. First pass - Raw data - extract relevant lines of data - put in list
    possible types = CSV , sysinfo, DriverTrace, 
4. Do the actual analysis 
    - DriverTrace packet timing
    - Device history -
    - Server restarts 
'''
from LogFile import *
from RawData import *
from CSV import *
#import time
#ticks1 = time.time()
#f = LogFile("..\logs\CaseMI_modbus_issue_10lines_quotes.csv","CSV")
f = LogFile("~/Documents/citectlogs/kdump1.dat","CSV")
#f.__dict__
# now with file object, pass in Regex or let object do that?
if f.fh != None :
    oRawCSV = RawData(f,"CSV")
    iT = oRawCSV.lCnt[0]
    iM = oRawCSV.lCnt[1]
    print('matched {} lines out of {} ' .format(iM,iT))
    print(oRawCSV.lRaw[:2])
    oResCSV = CSV(oRawCSV.lRaw,'freq')
    iT = oResCSV.lCnt[0]
    iM = oResCSV.lCnt[1]
    print('matched {} lines out of {} ' .format(iM,iT))
#print('this run took {} ms' .format((ticks2-time.time())*1000))
          
else :
    print("Raté")          
