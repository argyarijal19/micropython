from machine import Pin
from utime import sleep

led = Pin(4, Pin.OUT)

def led_on():
    led.on()
    
def read_sensor():
    led.on()
    sleep(0.2)
    led.off()
    sleep(0.1)
    