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

sql = ("SELECT p.moisture, p.temperature, strftime('%Y-%m-%d %H:%M:%S',m.time) FROM payload_temp_moisture p, metadata m WHERE m.message_id = p.message_id")

conn = sqlite3.connect('messages.db')
c = conn.cursor()

graphArrayTemperature = []
graphArrayMoisture = []
for row in c.execute(sql):
    startingInfo = str(row).replace(')','').replace('(','').replace('u\'','').replace("'","")
    splitInfo = startingInfo.split(',')
    #plot columns 3 (time) and 5 (rssi)
    graphArrayAppendTemperature = splitInfo[2]+','+splitInfo[1]
    graphArrayTemperature.append(graphArrayAppendTemperature)
    graphArrayAppendMoisture = splitInfo[2]+','+splitInfo[0]
    graphArrayMoisture.append(graphArrayAppendMoisture)

c.close()
conn.close()
timestamp1, temperature = np.loadtxt(graphArrayTemperature, delimiter=',', unpack=True,
        converters={0: bytespdate2num(' %Y-%m-%d %H:%M:%S')})

timestamp2, moisture = np.loadtxt(graphArrayMoisture, delimiter=',', unpack=True,
        converters={0: bytespdate2num(' %Y-%m-%d %H:%M:%S')})

labels=[]
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot_date(timestamp1, temperature, 'g.')
labels.append('temperature')
ax2.plot_date(timestamp2, moisture, 'b.')
labels.append('moisture')

ax1.set_xlabel('DateTime')
ax1.set_ylabel('Temperature', color='g')
ax2.set_ylabel('Moisture', color='b')

plt.show()   


