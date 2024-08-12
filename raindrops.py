from machine import Pin, ADC
import time

POWER_PIN = 32
DO_PIN = 13
#AO_PIN = 33

power_pin = Pin(POWER_PIN, Pin.OUT)
do_pin = Pin(DO_PIN, Pin.IN)
def get_rain_sensor():
    power_pin.value(1)
    time.sleep_ms(10)
    rain_state = do_pin.value()
    power_pin.value(0)
    print(do_pin.value())
    if do_pin.value() == 0:
        print("The rain is NOT detected")
    else:
        print("The rain is detected")
    
    time.sleep(1)
    return rain_state

