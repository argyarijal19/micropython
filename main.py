from mqtt import connect_mqtt, publish
from web_server import selfConnetcted, processing_web
from dht22 import getData
from led_controller import led_on, read_sensor
from battery_log import battery_log
from rain_data import get_rain_sensor
from systemInfo import get_free_memory, measure_cpu_load
from bme_read import read_pressure
import urequests as requests
import uasyncio as asyncio
import time
import gc
import machine

async def send_sensor_data():
    while True:
        led_on()
        checkPress, press, temp = read_pressure()
        checkHum, humd = getData()
        checkRain, rain = get_rain_sensor()
        
        data = {
            "temperature": temp,
            "humidity": humd,
            "message": "data inserted",
            "rain_was_fall": rain,
            "pressure": press
            }
        response = requests.post("https://rainfall-be.techlabcode.cloud/data", json=data)
        print(response.text)
        response.close()
        await asyncio.sleep(5)
        

async def send_system_info():
    SERVER = "193.203.167.97"
    PORT = 1883
    USERNAME = "argyarijal"
    PASSWORD = "argyarijal"
    client = connect_mqtt("ta", SERVER, PORT, USERNAME, PASSWORD)
    
    while True:
        cpuMon = measure_cpu_load()
        ramMon = get_free_memory()
        checkPress, press, temp = read_pressure()
        checkHum, humd = getData()
        checkRain, rain = get_rain_sensor()
        battery = battery_log()
        totalSensor = 0
        
        if checkPress != 0 :
            totalSensor +=1
        if checkHum != 0:
            totalSensor +=1
        if checkRain != 0:
            totalSensor +=1
        print(totalSensor)
            
        publish(client, "rainfall/sensor", checkRain, checkHum, checkPress, totalSensor, str(ramMon), str(cpuMon), battery)
        await asyncio.sleep(5)
        
        
async def main():
    selfConnetcted()
    await asyncio.create_task(processing_web())
    task1 = asyncio.create_task(send_sensor_data())
    task2 = asyncio.create_task(send_system_info())
    
    # Wait indefinitely, tasks run continuously
    await task2
    await task1
    

gc.collect()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())