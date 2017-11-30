import inspect
import time
import json
import socket
import wmi
import os
import win32con
import win32api
import urllib.request
from sqlite3 import dbapi2 as sqlite3
db = sqlite3.connect("test.db")
db.commit()
cur=db.cursor()


class mon:
    def __init__(self):
        self.data = {}

    def getTime(self):
        return str(int(time.time()) + 8 * 3600)

    def getHost(self):
        return socket.gethostname()

    def getMemTotal(self):
        c = wmi.WMI()
        for sys in c.Win32_OperatingSystem():
            return sys.TotalVisibleMemorySize

    def getMemUsage(self):
        c = wmi.WMI()
        for sys in c.Win32_OperatingSystem():
            total = sys.TotalVisibleMemorySize
            free = sys.FreePhysicalMemory
            usage = int(total) - int(free)
            # print()
            return str(usage)

    def getMemFree(self):
        c = wmi.WMI()
        for sys in c.Win32_OperatingSystem():
            return sys.FreePhysicalMemory

    def runAllGet(self):
        for fun in inspect.getmembers(self, predicate=inspect.ismethod):
            # for fun in [getTime,getHost,getMemtotal,getMemUsage,getMemFree]:
            # print(fun[:3])
            if fun[0][:3] == 'get':
                # print(fun[:3])
                self.data[fun[0][3:]] = fun[1]()
                # print(self.data)
        return self.data

def Insert_data():
    m = mon()
    values = m.runAllGet()
    sql = "INSERT INTO memory (host,mem_free,mem_usage,mem_toeal,time) VALUES('%s', '%s', '%s', '%s', '%d')" % (
    values['Host'], values['MemFree'], values['MemUsage'], values['MemTotal'], int(values['Time']))
    ret=cur.execute(sql)
    db.commit()
    selec = "SELECT * from memory"
    qq = cur.execute(selec)
    valu= cur.fetchall()
    print(valu)

    #print(ret)
    #print(values)
while True:
    time.sleep(1)
    Insert_data()