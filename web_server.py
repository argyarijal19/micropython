import network
import socket
from time import sleep
import uasyncio as asyncio
import urequests as requests
from battery_log import battery_log



def selfConnetcted():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='ESP32-AP', password='12345678')
    print('Access point started: ', ap.ifconfig())
    return ap

def html_page(success=True):
    if success:
        html = """
        <html>
            <head><title>ESP32 WiFi Setup</title></head>
            <body>
                <h1>WiFi Setup</h1>
                <form action="/" method="post">
                    <input type="text" placeholder="Enter WiFi SSID" name="ssid"><br>
                    <input type="password" placeholder="Enter WiFi Password" name="password"><br>
                    <input type="submit" value="Connect">
                </form>
            </body>
        </html>
        """
    else:
        html = """
        <html>
            <head><title>ESP32 WiFi Setup</title></head>
            <body>
                <h1>Connection Failed</h1>
                <p>Failed to connect. Please check your credentials and try again.</p>
                <a href="/">Try Again</a>
            </body>
        </html>
        """
    return html

def html_page_success():
    html = """
        <html>
            <head><title>ESP32 WiFi Setup</title></head>
            <body>
                <h1>Connection Success</h1>
                <p>Enjoy Your Life.</p>
            </body>
        </html>
        """
    return html

def url_decode(encoded_str):
    decoded_str = encoded_str.replace('+', ' ')
    # Tambahkan decoding untuk karakter lainnya jika perlu
    return decoded_str

async def processing_web():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024).decode()
        headers, body = request.split('\r\n\r\n', 1)
        print('Headers:\n', headers)
        print('Body:\n', body)

        ssid_start = body.find('ssid=')
        password_start = body.find('password=')
        if ssid_start != -1 and password_start != -1:
            ssid_end = body.find('&', ssid_start)
            ssid_value = body[ssid_start+5:ssid_end] if ssid_end != -1 else body[ssid_start+5:]
            password_end = body.find('&', password_start)
            password_value = body[password_start+9:password_end] if password_end != -1 else body[password_start+9:]

            # URL decode the SSID and password
            ssid_value = url_decode(ssid_value)
            password_value = url_decode(password_value)

            print("=========PASSWORD VALUE ======> ", password_value)
            print("=========PASSWORD LENGTH ======> ", len(password_value))
            print("=========SSID VALUE ======> ", ssid_value)
            print("=========SSID LENGTH ======> ", len(ssid_value))

            sta = network.WLAN(network.STA_IF)
            sta.active(True)
            sta.connect(ssid_value, password_value)
            
            attempts = 0
            while not sta.isconnected() and attempts < 10:
                print("Attempting to connect...")
                sleep(1)
                attempts += 1
            
            # Check if the connection was successful
            if sta.isconnected():
                battery = battery_log()
                response = requests.post(f"https://rainfall-be.techlabcode.cloud/connect?battery={battery}")
                print(response.text)
                response.close()
                print('Connected to WiFi:', sta.ifconfig())
                response = html_page_success()
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall(response)
                conn.close()
                break
                return True
            else:
                print('Failed to connect.')
                response = html_page(False)
                sleep(3)
        else:
            response = html_page()

        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()


