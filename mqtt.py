from umqtt.simple import MQTTClient
import ussl as ssl
import ujson
import time

def connect_mqtt(client_id, SERVER, PORT, USERNAME, PASSWORD):
    client = MQTTClient(client_id, SERVER, PORT, USERNAME, PASSWORD)
    client.connect()
    return client

def publish(client, TOPIC, rain, dht, bmp, total_sensor, ram_consume, cpu_consume, batrey):
        data = {
            "total_sensor": total_sensor,
            "ram_consume": ram_consume,
            "cpu_consume": cpu_consume,
            "battery_level": batrey,
            "bmp180_sensor": bmp,
            "dht_sensor": dht,
            "rain_sensor": rain,
        }
        json_data = ujson.dumps(data)
        client.publish(TOPIC, json_data)
    
