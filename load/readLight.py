import smbus
import board
import busio
import adafruit_adxl34x

DEVICE = 0x23
POWER_DOWN = 0x00
POWER_ON = 0x01
RESET = 0x07
ONE_TIME_HIGH_RES_MODE = 0x20

bus = smbus.SMBus(1)
i2c = busio.I2C(board.SCL, board.SDA)

def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE)
    return ((data[1] + (256 * data[0])) / 1.2)

accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_motion_detection(threshold=25)

def checkForMovement():
    if accelerometer.events['motion']:
        return True
    return False