from machine import Pin
import dht

sensor = dht.DHT22(Pin(2))

def getData():
    try:
        sensor.measure()
        hum = sensor.humidity()
        print(hum)
        return (1, hum)
    except OSError as e:
        print("error", e)
        return (0, None)

