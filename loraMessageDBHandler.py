import sqlite3
import traceback
import sys
import UWAFarmConfiguration as UWAFarm

class loraMessage(object):
    '''
    classdocs
    '''

    dbName = UWAFarm.TTN_MQTT_DB_NAME
    GPS_APP_ID = UWAFarm.TTN_MQTT_USER_NAME_GPS
    TEMP_MOISTURE_APP_ID = UWAFarm.TTN_MQTT_USER_NAME_TM

    def __init(self):
        '''
        Constructor
        '''

    def getDevKeyByDevName(self, pDevName):
        lDevKey = -1
        cnx = sqlite3.connect(self.dbName)
        cursor = cnx.cursor()

        query = ("SELECT dev_key "
                "FROM devices "
                "WHERE dev_id = ?")

        cursor.execute(query, (pDevName,))
        
        for (dev_key) in cursor:
            lDevKey = dev_key

        cursor.close()
        cnx.close()
        return lDevKey

    def getAppKeyByAppID(self, pAPPID):
        lAppKey = -1
        cnx = sqlite3.connect(self.dbName)
        cursor = cnx.cursor()

        query = ("SELECT app_key "
                "FROM applications "
                "WHERE app_id = ?")

        cursor.execute(query, (pAPPID,))
        
        for (app_key) in cursor:
            lAppKey = app_key

        cursor.close()
        cnx.close()
        return lAppKey

    def getGatewayKeyByGtwID(self, pGTWID):
        lGTWKey = -1
        cnx = sqlite3.connect(self.dbName)
        cursor = cnx.cursor()

        query = ("SELECT gtw_key "
                "FROM gateway "
                "WHERE gtw_id = ?")

        cursor.execute(query, (pGTWID,))
        
        for (gtw_key) in cursor:
            lGTWKey = gtw_key

        cursor.close()
        cnx.close()
        return lGTWKey

    def insertNewDevKey(self, pDevID, pHardwareSerial):
        cnx = sqlite3.connect(self.dbName)
        cursor = cnx.cursor()

        insertDev = ("INSERT INTO devices(dev_id, hardware_serial) VALUES (?, ?)")
        cursor.execute(insertDev, (pDevID, pHardwareSerial))
        lDevKey =  cursor.lastrowid
        cursor.close()
        cnx.commit()
        cnx.close()
        return lDevKey

    def insertNewAppKey(self, pAppID):
        cnx = sqlite3.connect(self.dbName)
        cursor = cnx.cursor()

        insertApp = ("INSERT INTO applications(app_id) VALUES (?)")
        cursor.execute(insertApp, (pAppID,))
        lAppKey = cursor.lastrowid
        cursor.close()
        cnx.commit()
        cnx.close()
        return lAppKey

    def insertNewGateWay(self, pGateWayID, db):
        cursor = db.cursor()

        insertGateway = ("INSERT INTO gateway(gtw_id) VALUES (?)")
        cursor.execute(insertGateway, (pGateWayID,))
        lGateWayKey = cursor.lastrowid
        cursor.close()
        return lGateWayKey

    def insertValuesFromJSON(self, pJSONData, cursor, cnx):
        lDevKey = self.getDevKeyByDevName(pJSONData['dev_id'])
        if (lDevKey == -1):
            print("New Device Detected: ")
            print(pJSONData['dev_id'])
            lDevKey = self.insertNewDevKey(pJSONData['dev_id'], pJSONData['hardware_serial'])
        if (type(lDevKey) is tuple):
            lDevKey = lDevKey[0]

        lAppKey = self.getAppKeyByAppID(pJSONData['app_id'])
        if (lAppKey == -1):
            print("Warning, New App detected, I do not know how to save the payloads for this app type")
            print(pJSONData['app_id'])
            lAppKey = self.insertNewAppKey(pJSONData['app_id'])
        if (type(lAppKey) is tuple):
            lAppKey = lAppKey[0]

        #cnx = sqlite3.connect(self.dbName)

        #cursor = cnx.cursor()

        insertMessage = ("INSERT INTO message(app_id, dev_id, port, counter) VALUES (?, ?, ?, ?)")
        cursor.execute(insertMessage, (lAppKey, lDevKey, pJSONData['port'], pJSONData['counter']))
        lmessageID = cursor.lastrowid

        insertPayload = ("INSERT INTO payload(message_id, raw_payload) VALUES (?, ?)")
        cursor.execute(insertPayload,(lmessageID, pJSONData['payload_raw']))

        if (self.GPS_APP_ID == pJSONData['app_id']):
            insertGPSPayload = ("INSERT INTO payload_gps_data(message_id, alt, hdop, latitude, longitude) VALUES (?, ?, ?, ?, ?)")
            cursor.execute(insertGPSPayload, (lmessageID, pJSONData['payload_fields']['alt'], pJSONData['payload_fields']['hdop'], pJSONData['payload_fields']['lat'], pJSONData['payload_fields']['lon']))
        elif (self.TEMP_MOISTURE_APP_ID == pJSONData['app_id']):
            insertTempHumidityPayload = ("INSERT INTO payload_temp_moisture(message_id, moisture, port, temperature) VALUES (?, ?, ?, ?)")
            cursor.execute(insertTempHumidityPayload, (lmessageID, pJSONData['payload_fields']['moisture'], pJSONData['payload_fields']['port'], pJSONData['payload_fields']['temperature']))
        else:
            print("I don't know how to insert correct payload data for this app so dumping JSON into payload_unknown_app")
            insertPayloadUnknown = ("INSERT INTO payload_unknown_app(message_id, json_text) VALUES (?, ?)")
            cursor.execute(insertPayloadUnknown, (lmessageID, pJSONData['payload_fields']))

        insertMetadata = ("INSERT INTO metadata(message_id, time, frequency, modulation, data_rate, airtime, coding_rate) VALUES (?, ?, ?, ?, ?, ?, ?)")
        cursor.execute(insertMetadata, (lmessageID, pJSONData['metadata']['time'], pJSONData['metadata']['frequency'], pJSONData['metadata']['modulation'], pJSONData['metadata']['data_rate'], pJSONData['metadata']['airtime'], pJSONData['metadata']['coding_rate']))

        insertgatewayinfo = ("INSERT INTO gatewayinfo(gtw_key, message_id, time_stamp, time, channel, rssi, snr, rf_chain, latitude, longitude, altitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")

        for gateway_record in pJSONData['metadata']['gateways']:
            lGTWKey = self.getGatewayKeyByGtwID(gateway_record['gtw_id'])
            if (lGTWKey == -1):
                lGTWKey = self.insertNewGateWay(gateway_record['gtw_id'], cnx)
                print("New Gateway Detected:")
                print(gateway_record['gtw_id'])
            if (type(lGTWKey) is tuple):
                lGTWKey = lGTWKey[0]

            cursor.execute(insertgatewayinfo, (lGTWKey, lmessageID, gateway_record['timestamp'], gateway_record['time'], gateway_record['channel'], gateway_record['rssi'], gateway_record['snr'], gateway_record['rf_chain'], gateway_record['latitude'], gateway_record['longitude'], gateway_record['altitude']))

    def saveAll(self, pJSONData):
        cnx = sqlite3.connect(self.dbName)

        cursor = cnx.cursor()
        try:
            self.insertValuesFromJSON(pJSONData, cursor, cnx)
            cursor.close()
            cnx.commit()
            cnx.close()
        except KeyError:
            print(traceback.format_exc())
            print("Transmitter did not send correct data")
            cursor.close()
            cnx.rollback()
            cnx.close()
        except Exception:
            print(traceback.format_exc())
            try:
                #Attempt DB rollback
                cursor.close()
                cnx.rollback()
                cnx.close()
            except:
                print("System so bad rollback will not work, crashing out completely")
                raise










            










    

    


