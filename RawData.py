# File object is passed in here and first pass is made to extract relevant lines 
class RawData:
    
    def __init__(self, of=None, ftype=None):  #of = file object 
        import re
        self.ftype = ftype #full file name with path
        if ftype == 'CSV' :
            self.rgx = re.compile(r'.*(\d+).*\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b).*(\bQuery|Response\b).*')
        elif sFtype == 'syslog' :
            self.rgx = re.compile(r"(?P<date>[\d-]+)\s(?P<time>[\d:\.]+)\s.*DRIVERTRACE.*(?P<qtype>CTDRV_READ|CTDRV_STATUS_UNIT)(?P<lereste>.*)")
        else :
            print("echec - no valid file type")
        self.lRaw = ["vide"] # list of raw lines 
        if self.rgx != None :
            iT = 0
            iM = 0
            self.lRaw = []
            for sline in of.fh :
                iT+=1 #count total lines
                mymatch = self.rgx.match(sline)
                if mymatch :
                    iM+=1 #count matched lines
                    ltemp = mymatch.group(0) #some CSV exports have quotes, strip these out
                    ltemp = ltemp.replace('"','')
                    self.lRaw.append(ltemp)
            
        #print('matched {} lines out of {} ' .format(iM,iT))
        self.lCnt=[iT,iM]
                    
            

    def set_rgx(self, rgx):
        self.rgx = rgx
        
    def get_rgx(self):
        return self.rgx

    def get_lCnt(self):
        return self.lCnt

    def get_lRaw(self):
        return self.lRaw
