from machine import Pin
import time

POWER_PIN = 32
DO_PIN = 13

power_pin = Pin(POWER_PIN, Pin.OUT)
do_pin = Pin(DO_PIN, Pin.IN)

def get_rain_sensor():
    try:
        power_pin.value(1)
        time.sleep_ms(10)
        rain_state = do_pin.value()
        power_pin.value(0)
        if rain_state == 0:
            print("The rain is detected")
        else:
            print("The rain is NOT detected")
        return (1, rain_state)
    except Exception as e:
        return (0, None)
