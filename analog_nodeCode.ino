/*******************************************************************************
 * Copyright (c) 2015 Thomas Telkamp and Matthijs Kooijman
 *
 * Permission is hereby granted, free of charge, to anyone
 * obtaining a copy of this document and accompanying files,
 * to do whatever they want with them without any restriction,
 * including, but not limited to, copying, modification and redistribution.
 * NO WARRANTY OF ANY KIND IS PROVIDED.
 *
 * This example will send Temperature and Humidity
 * using frequency and encryption settings matching those of
 * the The Things Network. Application will 'sleep' 7x8 seconds (56 seconds)
 *
 * This uses OTAA (Over-the-air activation), where where a DevEUI and
 * application key is configured, which are used in an over-the-air
 * activation procedure where a DevAddr and session keys are
 * assigned/generated for use with all further communication.
 *
 * Note: LoRaWAN per sub-band duty-cycle limitation is enforced (1% in
 * g1, 0.1% in g2), but not the TTN fair usage policy (which is probably
 * violated by this sketch when left running for longer)!

 * To use this sketch, first register your application and device with
 * the things network, to set or generate an AppEUI, DevEUI and AppKey.
 * Multiple devices can use the same AppEUI, but each device has its own
 * DevEUI and AppKey.
 *
 * Do not forget to define the radio type correctly in config.h.
 *
 *******************************************************************************/

#include <avr/sleep.h>
#include <avr/wdt.h>
#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>
#include "LowPower.h"

#include <Arduino.h>

int sleepcycles = 1;  // every sleepcycle will last 8 secs, total sleeptime will be sleepcycles * 8 sec
bool joined = false;
bool sleeping = false;
#define RS485RE 8 
#define RS485DE 9 
#define AnalogSensorPowerEnable 4 

// This EUI must be in little-endian format, so least-significant-byte
// first. When copying an EUI from ttnctl output, this means to reverse
// the bytes. For TTN issued EUIs the last bytes should be 0xD5, 0xB3,
// 0x70.
 
//static const u1_t DEVEUI[8]  = { 0xA7, 0x23, 0xAA, 0x00, 0x57, 0xA3, 0x17, 0x00 };

//UWA node 1
//static const u1_t DEVEUI[8]  = { 0xAF, 0x77, 0x82, 0x0D, 0x3F, 0x33, 0x54, 0x00 };
//UWA node 2
//static const u1_t DEVEUI[8]  = { 0xB8, 0x42, 0x76, 0x81, 0x50, 0x15, 0x84, 0x00 };
//UWA node 3
static const u1_t DEVEUI[8]  = { 0x62, 0x5D, 0xD5, 0x8D, 0x9E, 0x85, 0x6C, 0x00 }; 
//UWA node 3
//static const u1_t DEVEUI[8]  = { 0x62, 0x5D, 0xD5, 0x8D, 0x9E, 0x85, 0x6C, 0x00 };
//UWA node 4
//static const u1_t DEVEUI[8]  = { 0xDD, 0x5E, 0x3A, 0x16, 0xEA, 0x8F, 0xED, 0x00 };
//UWA node 5
//static const u1_t DEVEUI[8]  = { 0xA9, 0x0E, 0x3D, 0x27, 0xE3, 0xFA, 0xF4, 0x00 };
//UWA node 7
//static const u1_t DEVEUI[8]  = { 0x62, 0x52, 0xAB, 0x6D, 0x1A, 0x83, 0x8A, 0x00 };



//Atif key
//static const u1_t DEVEUI[8]  = { 0x74, 0x35, 0x09, 0xDF, 0xE8, 0xDD, 0x72, 0x00 };


//Achtung node 6 fehlt, 3 doppelt!!!


//APPEUI ist always the same
static const u1_t APPEUI[8] = { 0x7E, 0xBA, 0x00, 0xD0, 0x7E, 0xD5, 0xB3, 0x70 };
//Atif App Key
//static const u1_t APPEUI[8] = { 0x07, 0x0A, 0x01, 0xD0, 0x7E, 0xD5, 0xB3, 0x70 };

// This key should be in big endian format (or, since it is not really a
// number but a block of memory, endianness does not really apply). In
// practice, a key taken from ttnctl can be copied as-is.
// The key shown here is the semtech default key.
//static const u1_t APPKEY[16] = { 0x99, 0x37, 0x6E, 0xF1, 0xF3, 0x86, 0x26, 0x01, 0xD2, 0x1E, 0x67, 0xEE, 0x3D, 0x79, 0xF6, 0x3A };

//UWA node 1
//static const u1_t APPKEY[16] = { 0x6A, 0xF7, 0x26, 0x1B, 0x55, 0xA4, 0x12, 0x5C, 0x2F, 0xFE, 0xF4, 0xEF, 0x6B, 0x2C, 0x67, 0x10 };
//UWA node 2
//static const u1_t APPKEY[16] = { 0x47, 0x17, 0xFD, 0x01, 0xAA, 0xBE, 0xD7, 0xFA, 0xBB, 0x31, 0xF2, 0x3E, 0xE3, 0x09, 0x0D, 0xF9 };
//UWA node 3
static const u1_t APPKEY[16] = { 0xA3, 0x71, 0xF5, 0x20, 0x12, 0xAF, 0xFB, 0x3C, 0xEA, 0x23, 0x80, 0xE5, 0x0B, 0x5F, 0xBA, 0x1D };
//UWA node 4
//static const u1_t APPKEY[16] = { 0x31, 0xE1, 0x1E, 0x18, 0xE2, 0xA8, 0x29, 0xFE, 0x4E, 0xD5, 0xA0, 0x15, 0x59, 0x7E, 0x1F, 0xEC };
//UWA node 5
//static const u1_t APPKEY[16] = { 0x1D, 0x99, 0xDB, 0x55, 0xDA, 0x72, 0x21, 0x8D, 0xC8, 0xFD, 0x96, 0xA8, 0x98, 0x55, 0x22, 0x67 };
//UWA node 6
//static const u1_t APPKEY[16] = { 0x2A, 0x05, 0x36, 0xBE, 0x97, 0x2E, 0x2B, 0xA9, 0x81, 0xC8, 0x85, 0xD4, 0x7B, 0xC8, 0x0D, 0x4A };
//UWA node 7
//static const u1_t APPKEY[16] = { 0xFC, 0xF6, 0xC0, 0xE0, 0x59, 0x54, 0x4C, 0x7A, 0x2A, 0x1F, 0xD0, 0x83, 0x3A, 0xBA, 0xE7, 0x6A };

//Atif key
//static const u1_t APPKEY[16] = { 0x47, 0x17, 0xFD, 0x01, 0xAA, 0xBE, 0xD7, 0xFA, 0xBB, 0x31, 0xF2, 0x3E, 0xE3, 0x09, 0x0D, 0xF9 };


// provide APPEUI (8 bytes, LSBF)
void os_getArtEui (u1_t* buf) {
  memcpy(buf, APPEUI, 8);
}

// provide DEVEUI (8 bytes, LSBF)
void os_getDevEui (u1_t* buf) {
  memcpy(buf, DEVEUI, 8);
}

// provide APPKEY key (16 bytes)
void os_getDevKey (u1_t* buf) {
  memcpy(buf, APPKEY, 16);
}

static osjob_t sendjob;
static osjob_t initjob;

// Pin mapping is hardware specific.
// Pin mapping
const lmic_pinmap lmic_pins = {
    .nss = 10,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 6,
    .dio = {5,3, LMIC_UNUSED_PIN}, //DIO0 and DIO1 connected    
};

const int measurements = 50;

void onEvent (ev_t ev) {
  int i,j;
  switch (ev) {
    case EV_SCAN_TIMEOUT:
      Serial.println(F("EV_SCAN_TIMEOUT"));
      break;
    case EV_BEACON_FOUND:
      Serial.println(F("EV_BEACON_FOUND"));
      break;
    case EV_BEACON_MISSED:
      Serial.println(F("EV_BEACON_MISSED"));
      break;
    case EV_BEACON_TRACKED:
      Serial.println(F("EV_BEACON_TRACKED"));
      break;
    case EV_JOINING: 
      Serial.println(F("EV_JOINING"));
      break;
    case EV_JOINED:
      Serial.println(F("EV_JOINED"));
      // Disable link check validation (automatically enabled
      // during join, but not supported by TTN at this time).
      LMIC_setLinkCheckMode(0);
      //digitalWrite(LedPin,LOW);
      // after Joining a job with the values will be sent.
      joined = true;
      break;
    case EV_RFU1:
      Serial.println(F("EV_RFU1"));
      break;
    case EV_JOIN_FAILED:
      Serial.println(F("EV_JOIN_FAILED"));
      break;
    case EV_REJOIN_FAILED:
      Serial.println(F("EV_REJOIN_FAILED"));
      // Re-init
      os_setCallback(&initjob, initfunc);      
      break;
    case EV_TXCOMPLETE:
      sleeping = true;
        if (LMIC.dataLen) {
        // data received in rx slot after tx
        // if any data received, a LED will blink
        // this number of times, with a maximum of 10
        Serial.print(F("Data Received: "));
        Serial.println(LMIC.frame[LMIC.dataBeg],HEX);
        i=(LMIC.frame[LMIC.dataBeg]);
        // i (0..255) can be used as data for any other application
        // like controlling a relay, showing a display message etc.
      }
      Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
      delay(50);  // delay to complete Serial Output before Sleeping

      // Schedule next transmission
      // next transmission will take place after next wake-up cycle in main loop
      break;
    case EV_LOST_TSYNC:
      Serial.println(F("EV_LOST_TSYNC"));
      break;
    case EV_RESET:
      Serial.println(F("EV_RESET"));
      break;
    case EV_RXCOMPLETE:
      // data received in ping slot
      Serial.println(F("EV_RXCOMPLETE"));
      break;
    case EV_LINK_DEAD:
      Serial.println(F("EV_LINK_DEAD"));
      break;
    case EV_LINK_ALIVE:
      Serial.println(F("EV_LINK_ALIVE"));
      break;
    default:
      Serial.println(F("Unknown event"));
      break;
  }
}

void do_send(osjob_t* j) {
  byte buffer[4];  

  float temperatureArray[measurements];
  float sensorValueTemperature = 0.0;
  float moistureArray[measurements];
  float sensorValueMoisture = 0.0;

  digitalWrite(RS485RE,HIGH); 
  digitalWrite(RS485DE,HIGH);  
  digitalWrite(AnalogSensorPowerEnable,HIGH); 
  delay(300);  //small delay to power up
  Serial.println();

  for (int i = 0; i < measurements; i++)
  {
    temperatureArray[i] = analogRead(A0); 
    moistureArray[i] = analogRead(A1); 
  }
  
  for (int i = 0; i < measurements; i++)
  {
    sensorValueTemperature += temperatureArray[i];
    sensorValueMoisture += moistureArray[i];
  }
  
  sensorValueTemperature = sensorValueTemperature / measurements;
  sensorValueMoisture = sensorValueMoisture / measurements;

  sensorValueTemperature = sensorValueTemperature*3.3/1024;
  sensorValueMoisture = sensorValueMoisture *3.3/1024;
  
  sensorValueTemperature = (sensorValueTemperature-0.5)*100;
  sensorValueMoisture = sensorValueMoisture *50/3;
  
  sensorValueTemperature = sensorValueTemperature*10;
  sensorValueMoisture = sensorValueMoisture*10;
  
  uint16_t temperature_int = sensorValueTemperature;
  uint16_t moisture_int = sensorValueMoisture; 

  Serial.println(sensorValueTemperature);  
  Serial.println(sensorValueMoisture);   
  Serial.println(temperature_int);  
  Serial.println(moisture_int);    
  digitalWrite(AnalogSensorPowerEnable,LOW); 
    
        buffer[0]=highByte(temperature_int) ; //higher byte
        buffer[1]=lowByte(temperature_int);   //lower byte
        buffer[2]=highByte(moisture_int) ; //higher byte
        buffer[3]=lowByte(moisture_int);   //lower byte        
    // Check if there is not a current TX/RX job running
  if (LMIC.opmode & OP_TXRXPEND) {
    Serial.println(F("OP_TXRXPEND, not sending"));
  } else {
    // Prepare upstream data transmission at the next possible time.
    LMIC_setTxData2(1, (uint8_t*) buffer, 4 , 0);
    Serial.println(F("Sending: "));
  }
}

// initial job
static void initfunc (osjob_t* j) {
    // reset MAC state
    LMIC_reset();
    // start joining
    LMIC_startJoining();
    // init done - onEvent() callback will be invoked...
}

void setup()
  {
  digitalWrite(RS485RE,HIGH); 
  digitalWrite(RS485DE,HIGH);     
  Serial.begin(9600);
  Serial.println(F("Starting"));
  os_init();
  // Reset the MAC state. Session and pending data transfers will be discarded.
  os_setCallback(&initjob, initfunc);
  LMIC_reset();
}


void loop()
{
    // start OTAA JOIN
    if (joined==false)
    {

      os_runloop_once();
      
    }
    else
    {     
      do_send(&sendjob);    // Sent sensor values
      while(sleeping == false)
      {
        os_runloop_once();
      }
      sleeping = false;
      for (int i=0;i<sleepcycles;i++)
      {
          digitalWrite(RS485RE,HIGH); 
          digitalWrite(RS485DE,LOW);   
          LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);    //sleep 8 seconds
      }
    }
      
      //digitalWrite(LedPin,((millis()/100) % 2) && (joined==false)); // only blinking when joining and not sleeping
    
}


