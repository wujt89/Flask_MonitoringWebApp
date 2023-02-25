from flask import Flask, render_template, url_for, request, redirect
from turbo_flask import Turbo
from time import sleep
import threading
import json
import sqlite3
from datetime import datetime
# from readLight import readLight, checkForMovement


app = Flask(__name__, static_folder='/Users/wujt/Desktop/examples/load/static')
turbo = Turbo(app)

IRObSensorsTable = ('SensorIR1Ob', 'SensorIR2Ob',
                    'SensorIR3Ob', 'SensorIR4Ob', 'SensorIR5Ob', 'SensorIR6Ob',
                    'SensorIR7Ob', 'SensorIR8Ob')
IRAmSensorsTable = ('SensorIR1Am', 'SensorIR2Am',
                    'SensorIR3Am', 'SensorIR4Am', 'SensorIR5Am', 'SensorIR6Am',
                    'SensorIR7Am', 'SensorIR8Am')
DSSensorsTable = ('SensorDS1', 'SensorDS2',
                  'SensorDS3', 'SensorDS4', 'SensorDS5', 'SensorDS6',
                  'SensorDS7', 'SensorDS8')

sensorInfoGET = {
    'SensorDS': 'null',
    'SensorAM': 'SensorIR2Am',
    'SensorOB': 'SensorIR2Ob'
}

flag = 0
lastRead = ''


def fetchingChartDatafromSQL(elementName, limit):
    conn = sqlite3.connect('sensors.db')
    element = elementName
    query = f'''SELECT {element} FROM(
    SELECT timestamp, {element} FROM sensors ORDER BY timestamp DESC LIMIT {limit})
    ORDER BY timestamp ASC'''
    c = conn.cursor()
    c.execute(query)
    fetched = c.fetchall()
    conn.commit()
    conn.close()
    table = []
    for i in range(limit):
        table.append(fetched[i][0])
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


def fetchingAlertDatafromSQL():
    conn = sqlite3.connect('sensors.db')
    query = f'''SELECT * FROM alertsValues LIMIT 1'''
    c = conn.cursor()
    c.execute(query)
    table = c.fetchall()
    conn.commit()
    conn.close()
    return table


def fetchingColumnDatafromSQL():
    conn = sqlite3.connect('sensors.db')
    query = f'''SELECT * FROM sensors LIMIT1 '''
    table = []
    c = conn.cursor()
    data = c.execute(query)
    for column in data.description:
        table.append(column[0])
    conn.commit()
    conn.close()
    return table



def updateChart():
    chartValue = ''
    global sensorInfoGET
    if sensorInfoGET['SensorDS'] != 'null':
        chartValue = sensorInfoGET['SensorDS']
        tableFirst = fetchingChartDatafromSQL(chartValue, 50)
        timeTable = fetchingChartDatafromSQL('timestamp', 50)
        turbo.push(turbo.replace(render_template(
            'chartDSDiv.html', labels=timeTable, valuesDS=tableFirst), 'chart'))
    else:
        chartValue = [sensorInfoGET['SensorOB'], sensorInfoGET['SensorAM']]
        tableFirst = fetchingChartDatafromSQL(chartValue[0], 50)
        tableSecond = fetchingChartDatafromSQL(chartValue[1], 50)
        timeTable = fetchingChartDatafromSQL('timestamp', 50)
        turbo.push(turbo.replace(render_template(
            'chartsDiv.html', labels=timeTable, values=tableFirst, values2=tableSecond), 'chart'))

def updateLogTemp():
    now = datetime.now()
    timeNow = now.strftime("%d/%m/%Y %H:%M:%S")
    message = timeNow + " " + "Temperature read"
    return timeNow, message


def updateLogCam():
    now = datetime.now()
    timeNow = now.strftime("%d/%m/%Y %H:%M:%S")
    message = timeNow + " " + "Photo has been captured"
    return timeNow, message


def updateLogMot():
    now = datetime.now()
    timeNow = now.strftime("%d/%m/%Y %H:%M:%S")
    message = timeNow + " " + "Object has moved"
    return timeNow, message


def updateLogDoor():
    now = datetime.now()
    timeNow = now.strftime("%d/%m/%Y %H:%M:%S")
    message = timeNow + " " + "Door opened"
    return timeNow, message

def createOKAndNOKTablesForMap():
    buttonOk = []
    buttonNok = []
    tableMap = fetchingMapDatafromSQL()
    tableAlerts = fetchingAlertDatafromSQL()
    tablenames = fetchingColumnDatafromSQL()
    for j in range(23):
        j=j+1
        if tableMap[0][j] > tableAlerts[0][j]:
            buttonNok.append(tablenames[j])
        else:
            buttonOk.append(tablenames[j])

    return buttonNok, buttonOk

def updateMap():
    buttons = createOKAndNOKTablesForMap()
    turbo.push(turbo.replace(render_template(
        'map.html', buttonOk=buttons[1], buttonNok=buttons[0]), 'map'))


def updateLogAlarm():
    buttons = createOKAndNOKTablesForMap()
    now = datetime.now()
    timeNow = now.strftime("%d/%m/%Y %H:%M:%S")
    message = timeNow + " " + "Alarms detected on sensors: "
    numb = len(buttons)
    for item in buttons[0]:
        message = message + item + " "
    return timeNow, message, numb

def addLogToSQL(timeNow, mess):
    conn = sqlite3.connect('sensors.db')
    c = conn.cursor()
    c.execute(
        """INSERT INTO logs (timestamp, Log) VALUES (?, ?)""",
        (timeNow, mess))
    conn.commit()
    conn.close()

def checkForNewEntry():
    global lastRead
    conn = sqlite3.connect('sensors.db')
    c = conn.cursor()
    query = f'''SELECT timestamp FROM sensors ORDER BY timestamp DESC LIMIT 1 '''
    c.execute(query)
    conn.commit()
    p = c.fetchall()
    conn.close()
    print(p)
    print(lastRead)
    if p != lastRead:
        lastRead = p
        return True
    else:
        return False

@app.before_first_request
def before_first_request():
    threading.Timer(10.0, update_load).start()
    # threading.Timer(1.0, updateSensors).start()


@app.route('/', methods=['POST', 'GET'])
def index():
    buttons = createOKAndNOKTablesForMap()
    return render_template("index.html", buttonOk=buttons[1], buttonNok=buttons[0])


@app.route('/alert', methods=['POST', 'GET'])
def alert():
    conn = sqlite3.connect('sensors.db')
    c = conn.cursor()
    c.execute(
        """SELECT Log FROM logs ORDER BY timestamp DESC LIMIT 10000""")
    fetched = c.fetchall()
    conn.commit()
    conn.close()
    table = []
    for i in range(len(fetched)):
        table.append(fetched[i][0])
    return render_template("alert.html", table=table)


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    conn = sqlite3.connect('sensors.db')
    query = f'''SELECT photoName FROM(
    SELECT timestamp, photoName FROM photos ORDER BY timestamp DESC LIMIT 15)
    ORDER BY timestamp ASC'''
    c = conn.cursor()
    c.execute(query)
    fetched = c.fetchall()
    print(fetched)
    table = []
    for i in range(15):
        table.append(fetched[i][0])

    query = f'''SELECT timestamp FROM(
    SELECT timestamp FROM photos ORDER BY timestamp DESC LIMIT 15)
    ORDER BY timestamp ASC'''
    c.execute(query)
    fetchedTime = c.fetchall()
    conn.commit()
    conn.close()
    timeStamp = []
    for i in range(15):
        timeStamp.append(fetchedTime[i][0])
    return render_template('gallery.html', table=table, timeStamp=timeStamp)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != '####' or request.form['password'] != '####':
            error = 'Invalid Credentials. Please try again.'
            return redirect(url_for('/ '))
        else:
            return redirect(url_for('alert'))
    return render_template('login.html', error=error)

@app.route('/processSensorInfo/<string:sensorInfo>', methods=['POST'])
def processSensorInfo(sensorInfo):
    global sensorInfoGET
    sensorInfo = json.loads(sensorInfo)
    sensorInfoGET = sensorInfo
    updateChart()
    updateMap()
    return sensorInfo


@app.route('/processAlertInfo/<string:alertInfo>', methods=['POST'])
def processAlertInfo(alertInfo):
    alertInfo = json.loads(alertInfo)
    conn = sqlite3.connect('sensors.db')
    c = conn.cursor()
    element = alertInfo['sensor']
    value = alertInfo['value']
    query = f'''UPDATE alertsValues SET {element} = {value} WHERE SetValue = "Set1" '''
    c.execute(query)
    conn.commit()
    conn.close()
    return alertInfo


@app.context_processor
def inject_load():
    table = fetchingMapDatafromSQL()
    tableLimits = fetchingAlertDatafromSQL()
    IRSensorsStrings = []
    DSSensorsString = []
    for i in range(8):
        IRSensorsStrings.append(
            'Object: ' + str(table[0][i+1]) + ' Ambient: ' + str(table[0][i+9]) + ' Limit: ' + str(tableLimits[0][i+1]) + ', ' + str(tableLimits[0][i+9]))
        DSSensorsString.append('Ambient: ' + str(table[0][i+17]) + ' Limit: ' + str(tableLimits[0][i+17]))

    return {'time': table[0][0], 'SensorIR1': IRSensorsStrings[0], 'SensorIR2': IRSensorsStrings[1],
            'SensorIR3': IRSensorsStrings[2], 'SensorIR4': IRSensorsStrings[3], 'SensorIR5': IRSensorsStrings[4], 'SensorIR6': IRSensorsStrings[5],
            'SensorIR7': IRSensorsStrings[6], 'SensorIR8': IRSensorsStrings[7], 'SensorDS1': DSSensorsString[0], 'SensorDS2': DSSensorsString[1],
            'SensorDS3': DSSensorsString[2], 'SensorDS4': DSSensorsString[3], 'SensorDS5': DSSensorsString[4], 'SensorDS6': DSSensorsString[5],
            'SensorDS7': DSSensorsString[6], 'SensorDS8': DSSensorsString[7]}


def update_load():
    inject_load()
    with app.app_context():
        if checkForNewEntry():
            updateMap()
            updateChart()
            messageAlarm = updateLogAlarm()
            messageTemp = updateLogTemp()
            turbo.push(turbo.prepend(render_template(
                'read.html', message=messageTemp[1]), 'grid-item-3'))
            if messageAlarm[2]>0:
                turbo.push(turbo.prepend(render_template(
                    'alarm.html', message=messageAlarm[1]), 'grid-item-3'))

    threading.Timer(10.0, update_load).start()

# def updateSensors():
#     global flag
#     with app.app_context():
#         if readLight() > 50.0 and flag == 1:
#             now = datetime.now()
#             timeNow = now.strftime("%d/%m/%Y %H:%M:%S")
#             turbo.push(turbo.prepend(render_template(
#                 'door.html', time=timeNow), 'grid-item-3'))
#             turbo.push(turbo.prepend(render_template(
#                 'camera.html', time=timeNow), 'grid-item-3'))
#             flag = 0
#         elif readLight()<50.0  and flag == 0:
#             flag = 1

#         if checkForMovement():
#             now = datetime.now()
#             timeNow = now.strftime("%d/%m/%Y %H:%M:%S")
#             turbo.push(turbo.prepend(render_template(
#                 'move.html', time=timeNow), 'grid-item-3'))

   # threading.Timer(1.0, updateSensors).start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)