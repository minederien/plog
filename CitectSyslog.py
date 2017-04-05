''' Citect Syslog Analysis
    Some possibilities:
    1. Device based - count drivers and units coming online
    2. Offline incidents

    To optimize regex matching, a syslog will be divided into chunks representing
    each time the I/O server is restarted.  Then these chunks will be scanned to extract
    driver and device data.  So first step will be to capture all the I/O server start and stop
    events and the data in between. { Citect process is starting up(.*?)Citect process stopped }
    
# File object is passed in here and first pass is made to extract relevant lines 
'''
class CitectSyslog:
    
    def __init__(self, lRaw=None, antype=None):  #of = file object 
        import re
        import statistics
        self.antype = antype #type of analysis
        self.lFPass = lFPass #First pass, divide data into each time server is started  
        self.lRaw = lRaw
        self.lRes = [] #all extracted data 
        self.lCnt = None
        self.lStats = [] #
        
        if antype == 'freq' :
            self.rgx = re.compile(r'(\d+).*?(?P<time>[0-9]+\.?[0-9]+).*?\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b).*?\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b).+\s*(Query|Response):\s+Trans:\s+(?P<transno>\d+)')
        elif antype == 'devicestats' :
            self.rgx = re.compile(r"(?P<date>[\d-]+)\s(?P<time>[\d:\.]+)\s.*DRIVERTRACE.*(?P<qtype>CTDRV_READ|CTDRV_STATUS_UNIT)(?P<lereste>.*)")
        else :
            self.rgx = None
            print("echec - no valid file type passed in")
        # some CSV exports have quote marks around each field - clear these out
        print('inside CSV object with list containing {} elements' .format(len(self.lRaw)))
        # run first pass here        
            
        if self.rgx != None :
            iT = 0
            iM = 0
            iTran = 0
            print('{} lines passed in' .format(len(self.lRaw)))
            for sline in self.lRaw :
                #print(sline)
                iT+=1 #count total lines
                mymatch = self.rgx.match(sline)
                if mymatch :
                    iM+=1 #count matched lines
                    if iTran!=int(mymatch.group('transno')) :
                        iTran = int(mymatch.group('transno'))
                        fTime1= float(mymatch.group('time'))
                    else :
                        fTime2 = float(mymatch.group('time'))
                        fTranTime = (fTime2 - fTime1)*1000.0
                        lTmp = [iTran, fTime1, fTime2, fTranTime]
                        #self.lStats.append(lTmp) 
                        self.lRes.append(lTmp)
            self.lCnt=[iT,iM]
            lTime = []
            if self.lRes :
                for iTime in self.lRes :
                    lTime.append(iTime[3])
                fMean = statistics.mean(lTime)
                fStDev = statistics.stdev(lTime)
                print('query/response exchanges captured = ' + str(len(lTime)))
                print('ave response time = ' + str(fMean))
                print('std dev = ' + str(fStDev))
            
            
        else :
            print("no regex to work with")

            
        #print('matched {} lines out of {} ' .format(iM,iT))
                    
            

    def set_rgx(self, rgx):
        self.rgx = rgx
        
    def get_rgx(self):
        return self.rgx

    def get_lRaw(self):
        return self.lRaw

    def get_lRes(self):
        return self.lRes

    def get_lCnt(self):
        return self.lCnt


