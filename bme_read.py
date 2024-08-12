from machine import SoftI2C, Pin
from time import sleep
from BME280 import BMP280
# Define the pin numbers for SCL and SDA
scl_pin = Pin(22)
sda_pin = Pin(21)


# Initialize SoftI2C
i2c = SoftI2C(scl=scl_pin, sda=sda_pin, freq=10000)

def read_pressure():
    try:
        bmp = BMP280(i2c=i2c)
        temp = bmp.getTemp()
        press = bmp.getPress()
        print(temp)
        return (1, press, temp)
    except OSError as e:
        return (0, None, None)

    