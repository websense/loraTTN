import sqlite3
import time
import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

def getGraphData(pGtwKey, pDevId, db):

    sql = ("SELECT g.gtw_info_id, g.gtw_key, g.message_id, strftime('%Y-%m-%d %H:%M:%S',g.time), g.channel, g.rssi, g.snr FROM gatewayinfo g, message m WHERE g.gtw_key= ? and m.dev_id = ? and m.message_id = g.message_id")

    graphArray = []
    timestamp = []
    rssi = []
    e = db.cursor()
    for row in e.execute(sql, (pGtwKey,pDevId)):
        startingInfo = str(row).replace(')','').replace('(','').replace('u\'','').replace("'","")
        splitInfo = startingInfo.split(',')
        #plot columns 3 (time) and 5 (rssi)
        graphArrayAppend = splitInfo[3]+','+splitInfo[5]
        graphArray.append(graphArrayAppend)

    e.close()
    if len(graphArray) > 0:
        timestamp, rssi = np.loadtxt(graphArray, delimiter=',', unpack=True,
            converters={0: bytespdate2num(' %Y-%m-%d %H:%M:%S')})
        #converters={0: mdates.strpdate2num(' %Y-%m-%d %H:%M:%S')})
    return timestamp, rssi
    
labels=[]
conn = sqlite3.connect('messages.db')
c = conn.cursor()
gatewaySql = ("SELECT gtw_key, gtw_id FROM gateway")
deviceSql = ("SELECT dev_key, dev_id FROM devices")

for lDevice in c.execute(deviceSql):
    d = conn.cursor()
    for lGateway in d.execute(gatewaySql):
        timestamp, rssi = getGraphData(lGateway[0], lDevice[0], conn)
        plt.plot_date(timestamp, rssi)
        lLabelText = lDevice[1] + ' ' + lGateway[1]
        labels.append(lLabelText)
    d.close()        

c.close()
conn.close()

plt.xlabel('DateTime')
plt.ylabel('RSSI')
plt.legend(labels, ncol=4, loc='upper center', 
           bbox_to_anchor=[0.5, 1.1], 
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=True)
plt.show()   
