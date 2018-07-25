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

conn = sqlite3.connect('messages.db')
c = conn.cursor()

sql = ("SELECT gtw_info_id, gtw_key, message_id, strftime('%Y-%m-%d %H:%M:%S',time), channel, rssi, snr FROM gatewayinfo WHERE gtw_key=?")

graphArray = []
for row in c.execute(sql, (1,)):
    startingInfo = str(row).replace(')','').replace('(','').replace('u\'','').replace("'","")
    splitInfo = startingInfo.split(',')
    #plot columns 3 (time) and 5 (rssi)
    graphArrayAppend = splitInfo[3]+','+splitInfo[5]
    graphArray.append(graphArrayAppend)

timestamp1, rssi1 = np.loadtxt(graphArray, delimiter=',', unpack=True,
        converters={0: bytespdate2num(' %Y-%m-%d %H:%M:%S')})
        #converters={0: mdates.strpdate2num(' %Y-%m-%d %H:%M:%S')})

graphArray = []
for row in c.execute(sql, (2,)):
    startingInfo = str(row).replace(')','').replace('(','').replace('u\'','').replace("'","")
    splitInfo = startingInfo.split(',')
    #plot columns 3 (time) and 5 (rssi)
    graphArrayAppend = splitInfo[3]+','+splitInfo[5]
    graphArray.append(graphArrayAppend)

timestamp2, rssi2 = np.loadtxt(graphArray, delimiter=',', unpack=True,
        converters={0: bytespdate2num(' %Y-%m-%d %H:%M:%S')})
        #converters={0: mdates.strpdate2num(' %Y-%m-%d %H:%M:%S')})


c.close()
conn.close()
#fig = plt.figure()
#rect = fig.patch

#ax1 = fig.add_subplot(1,1,1, axisbg='white')
#plt.autoscale(enable=True)
#plt.plot(x=timestamp, y=rssi, fmt='b-', label = 'RSSI', linewidth=2)
labels=[]
plt.plot_date(timestamp1, rssi1)
labels.append(r'gateway1')
plt.plot_date(timestamp2, rssi2)
labels.append(r'gateway2')
plt.xlabel('DateTime')
plt.ylabel('RSSI')
plt.legend(labels, ncol=4, loc='upper center', 
           bbox_to_anchor=[0.5, 1.1], 
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=True)
plt.show()   
