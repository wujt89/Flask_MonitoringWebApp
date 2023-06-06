# Flask_MonitoringWebApp

The main object of this project is to monitor temperature and shocks in insustrial cabinets. The device is equiped with Raspberry Pi Camera HD that allows users to check who was the latest person that opened the cabinet.

Values from sensors are processed by STM32 board and send via UART to RasperryPi 3. Flask Server is hosted on RaspberryPi.
