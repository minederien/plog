# make sure file is viable, get some stats, future - determine if CSV or DAT 
class LogFile:
    
    def __init__(self, ffname=None, ftype=None):
        self.ffname = ffname #full file name with path
        self.ftype = ftype #CSV or DAT or etc.
        self.fh = None
        import platform
        import os
        import time
#        import re
        from stat import ST_SIZE,ST_MTIME
        self.plat = platform.system()
        print('OS = {}' .format(self.plat))
        if str.lower(self.plat) == 'windows' :
            sLogFolder = "logs\\"
        elif str.lower(self.plat) == 'linux' :
            sLogFolder = "logs\/"
            
        try:
            self.fh=open(ffname,  'r', errors='ignore')
            #print('self.fh = ', str(self.fh))
            st = os.stat(ffname)
            self.fsize = st[ST_SIZE]
            self.fmodt = st[ST_MTIME]
        except IOError as e:
            errno, strerror = e.args
            print("I/O error({0}): {1}".format(errno,strerror))
            print('kann Datei nicht öffnen:', ffname)
    
       
    def showprops(self):
        if self.ffname is not None :
            print("Hola, soy " + self.ffname)
            print("file modified:", self.fmodt)
        else:
            print("Hi, Ich bin einen Robot ohne Namen")
            
    def set_ffname(self, ffname):
        self.ffname = ffname
        
    def get_ffname(self):
        return self.ffname

    def get_fname(self):
        return self.fname

    def get_plat(self):
        return self.plat

    def get_fsize(self):
        self.fsize = st[ST_SIZE]
        return self.fsize

    def get_fmodt(self):
        return self.fmodt

    def get_fh(self):  # file handle 
        return self.fh
