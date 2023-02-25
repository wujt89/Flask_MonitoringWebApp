#!/usr/bin/python

import smbus
import board
import busio
import adafruit_adxl34x
import time
import serial
import threading
import sqlite3
import json
from datetime import datetime
from picamera import PiCamera
from app import addLogToSQL, updateLogAlarm, updateLogTemp, updateLogMot, updateLogCam, updateLogDoor

# connect to database
conn = sqlite3.connect('sensors.db')

# creating cursor
c = conn.cursor()

# creating table
c.execute("""CREATE TABLE IF NOT EXISTS sensors (
        timestamp DATATYPE,
        SensorIR1Ob DATATYPE,
        SensorIR2Ob DATATYPE,
        SensorIR3Ob DATATYPE,
        SensorIR4Ob DATATYPE,
        SensorIR5Ob DATATYPE,
        SensorIR6Ob DATATYPE,
        SensorIR7Ob DATATYPE,
        SensorIR8Ob DATATYPE,
        SensorIR1Am DATATYPE,
        SensorIR2Am DATATYPE,
        SensorIR3Am DATATYPE,
        SensorIR4Am DATATYPE,
        SensorIR5Am DATATYPE,
        SensorIR6Am DATATYPE,
        SensorIR7Am DATATYPE,
        SensorIR8Am DATATYPE,
        SensorDS1 DATATYPE,
        SensorDS2 DATATYPE,
        SensorDS3 DATATYPE,
        SensorDS4 DATATYPE,
        SensorDS5 DATATYPE,
        SensorDS6 DATATYPE,
        SensorDS7 DATATYPE,
        SensorDS8 DATATYPE
    ) """)

conn.commit()
conn.close()

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2000
)

data = 't'
dataSaved = ''

DEVICE = 0x23
POWER_DOWN = 0x00
POWER_ON = 0x01
RESET = 0x07
ONE_TIME_HIGH_RES_MODE = 0x20

counter = 0
camera = PiCamera()
bus = smbus.SMBus(1)
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_motion_detection(threshold=25)


def function():
    global counter
    if readLight() < 2.0:
        ser.write(str(data).encode())
        dataJson = ser.read()
        time.sleep(1)
        #data_left = ser.inWaiting()
        #dataJson += ser.read(data_left)
        while True:
            if len(dataJson) != 439:
                ser.write(str(data).encode())
                dataJson = ser.read()
                time.sleep(1)
                data_left = ser.inWaiting()
                dataJson += ser.read(data_left)
                print(len(dataJson))
                message = updateLogTemp()
                addLogToSQL(message[0], message[1])
                message = updateLogAlarm()
                addLogToSQL(message[0], message[1])
            else:
                break
        print(dataJson.decode(encoding='UTF-8'))
        y = json.loads(dataJson)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        conn = sqlite3.connect('sensors.db')
        c = conn.cursor()
        c.execute(
            """INSERT INTO sensors (timestamp, SensorIR1Ob, SensorIR2Ob,
            SensorIR3Ob, SensorIR4Ob, SensorIR5Ob, SensorIR6Ob, SensorIR7Ob,
            SensorIR8Ob, SensorIR1Am, SensorIR2Am, SensorIR3Am, SensorIR4Am,
            SensorIR5Am, SensorIR6Am, SensorIR7Am, SensorIR8Am, SensorDS1,
            SensorDS2, SensorDS3, SensorDS4, SensorDS5, SensorDS6, SensorDS7,
            SensorDS8) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ? ,?, ?, ?, ?)""",
            (dt_string, y['IR']['Sensor1'][0], y['IR']['Sensor2'][0], y['IR']['Sensor3'][0], y['IR']['Sensor4'][0], y['IR']['Sensor5'][0], y['IR']['Sensor6'][0], y['IR']['Sensor7'][0], y['IR']['Sensor8'][0], y['IR']['Sensor1'][1], y['IR']['Sensor2'][1], y['IR']['Sensor3'][1], y['IR']['Sensor4'][1], y['IR']['Sensor5'][1], y['IR']['Sensor6'][1], y['IR']['Sensor7'][1], y['IR']['Sensor8'][1], y['DS']['Sensor1'][0], y['DS']['Sensor2'][0], y['DS']['Sensor3'][0], y['DS']['Sensor4'][0], y['DS']['Sensor5'][0], y['DS']['Sensor6'][0], y['DS']['Sensor7'][0], y['DS']['Sensor8'][0]))

        conn.commit()
        conn.close()
    t = threading.Timer(10.0, function)
    t.start()


def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE)
    return ((data[1] + (256 * data[0])) / 1.2)


def main():
    global counter
    t = threading.Timer(5.0, function)
    t.start()
    while True:
        time.sleep(1)
        if readLight() > 50.0 and counter == 0:
            print(readLight())
            message = updateLogDoor()
            addLogToSQL(message[0], message[1])
            now = datetime.now()
            dt_string = now.strftime("%Y%m%d_%H:%M:%S")
            counter = 1
            time.sleep(2)
            camera.capture(f'/home/wujtvw/load/static/css/images/{dt_string}.jpg')
            photoNameSQ = dt_string + '.jpg'
            conn = sqlite3.connect('sensors.db')
            c = conn.cursor()
            c.execute(
            """INSERT INTO photos (timestamp, photoName) VALUES (?, ?)""",
            (dt_string, photoNameSQ))
            conn.commit()
            conn.close()
            message = updateLogCam()
            addLogToSQL(message[0], message[1])
        elif readLight() < 50 and counter == 1:
            counter = 0

        if accelerometer.events['motion']:
            print("Object has been moved")
            message = updateLogMot()
            addLogToSQL(message[0], message[1])


if __name__ == "__main__":
    main()