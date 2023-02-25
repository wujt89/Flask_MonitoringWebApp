import sqlite3
import json
from datetime import datetime 


def fethingDatafromSQL(elementName):
    conn = sqlite3.connect('sensors.db')
    element = elementName
    query = f'''SELECT {element} FROM(
    SELECT timestamp, {element} FROM sensors ORDER BY timestamp DESC LIMIT 3)
    ORDER BY timestamp ASC'''
    c = conn.cursor()
    c.execute(query)
    table = c.fetchall()
    conn.commit()
    conn.close()
    return table


def fetchingMapDatafromSQL():
    conn = sqlite3.connect('sensors.db')
    query = f'''SELECT * FROM sensors ORDER BY timestamp DESC LIMIT 1'''
    c = conn.cursor()
    c.execute(query)
    table = c.fetchall()
    conn.commit()
    conn.close()
    return table

dataJson = '{"IR": {"Sensor1": ["20.86", "21.68"], "Sensor2": ["20.95", "21.45"], "Sensor3": ["20.95", "21.35"], "Sensor4": ["20.80", "21.14"], "Sensor5": ["20.73", "20.64"], "Sensor6": ["20.73", "20.74"], "Sensor7": [ \
    "20.77", "20.86"], "Sensor8": ["21.01", "21.02"]}, "DS": {"Sensor1": ["20.25"], "Sensor2": ["20.68"], "Sensor3": ["20.50"], "Sensor4": ["20.43"], "Sensor5": ["20.12"], "Sensor6": ["19.56"], "Sensor7": ["19.43"], "Sensor8": ["20.50"]}}'
y = json.loads(dataJson)
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#connect to database
conn = sqlite3.connect('sensors.db')

#creating cursor
c = conn.cursor()

#creating table
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


c.execute("""CREATE TABLE IF NOT EXISTS photos (
        timestamp DATATYPE,
        photoName DATATYPE
    ) """)


c.execute("""CREATE TABLE IF NOT EXISTS alertsValues (
        SetValue DATATYPE,
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

c.execute("""CREATE TABLE IF NOT EXISTS logs (
        timestamp DATATYPE,
        Log DATATYPE
    ) """)

conn.commit()
conn.close()


# conn = sqlite3.connect('sensors.db')
# element = "SensorIR1Ob"
# query = f'''SELECT {element} FROM(
#     SELECT timestamp, {element} FROM sensors ORDER BY timestamp DESC LIMIT 3)
#     ORDER BY timestamp ASC'''
# c = conn.cursor()
# c.execute(query)

# table = c.fetchall()
# for item in range(len(table)):
#     print(table[item][0])
# conn.commit()
# conn.close()
# table=fethingDatafromSQL('SensorIR1OB')

# conn = sqlite3.connect('sensors.db')
# query = f'''SELECT * FROM sensors LIMIT 1'''
# c = conn.cursor()
# c.execute(query)
# table = c.fetchall()
# conn.commit()
# conn.close()


# for item in range(len(table)):
#     print(table)

# table = fetchingMapDatafromSQL()
# IRSensorsStrings = []
# DSSensorsString = []

# print(table[0][9])
# for i in range(8):
#     IRSensorsStrings.append('Ob: ' + str(table[0][i+1]) + ' Am: ' + str(table[0][i+9]))
#     DSSensorsString.append('Am: ' + str(table[0][i+17]))
# # print(c.fetchall()[len(c.fetchall())-1][0])

# print(table[0][0])
# print(DSSensorsString)

# conn = sqlite3.connect('sensors.db')
# c = conn.cursor()
# # c.execute(
# #     """INSERT INTO photos (timestamp, photoName) VALUES (?, ?)""",
# #     (dt_string, '05122022_04:25:05.jpg'))

# c.execute(
#     """INSERT INTO alertsValues (SetValue, SensorIR1Ob, SensorIR2Ob,
#     SensorIR3Ob, SensorIR4Ob, SensorIR5Ob, SensorIR6Ob, SensorIR7Ob,
#     SensorIR8Ob, SensorIR1Am, SensorIR2Am, SensorIR3Am, SensorIR4Am, 
#     SensorIR5Am, SensorIR6Am, SensorIR7Am, SensorIR8Am, SensorDS1, 
#     SensorDS2, SensorDS3, SensorDS4, SensorDS5, SensorDS6, SensorDS7, 
#     SensorDS8) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
#     ?, ?, ?, ?, ? ,?, ?, ?, ?)""",
#     ("Set1", 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100))

# conn.commit()
# conn.close()
