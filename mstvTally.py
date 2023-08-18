from machine import Pin
import password
import network
import time
import socket
import _thread


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.ifconfig(("192.168.1.141", "255.255.255.0", "192.168.1.1", "8.8.8.8"))
light = Pin(1, Pin.OUT)
light.value(0)
try:
    serverPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverPort.bind(('0.0.0.0', 2727))
    serverPort.listen(3)

    def checkConn():
        while True:
            if not wlan.isconnected():
                light.value(1)
                time.sleep(0.33)
                light.value(0)
                time.sleep(0.33)
                light.value(1)
                time.sleep(0.33)
                light.value(0)
                time.sleep(0.33)
                light.value(1)
                time.sleep(0.33)
                light.value(0)
                time.sleep(0.33)
                light.value(1)
                time.sleep(0.33)
                light.value(0)
                time.sleep(0.33)
            else:
                time.sleep(3)
            
            
            
    wlan.connect("ATT-WIFI-Mj4x", password.pw)
    time.sleep(1)
    while wlan.isconnected()==False:
            light.value(1)
            time.sleep(0.33)
            light.value(0)
            time.sleep(0.33)

    connTask=_thread.start_new_thread(checkConn, ())

    while True:
        

        client, addr = serverPort.accept()
        try:
            request = client.recv(1028).decode()
            
            if "GET /on" in request:
                light.value(1)
                client.sendall('HTTP/1.1 200 OK\nContent-Type: text/html\n\n' + "CAM1 ON")
            elif "GET /off" in request:
                light.value(0)
                client.sendall('HTTP/1.1 200 OK\nContent-Type: text/html\n\n' + "CAM1 OFF")
            elif "GET /favico" in request:
                client.sendall("HTTP/1.1 404")
        except Exception as e:
            print("Error:", e)
        finally:
            client.close()
finally:
    serverPort.close()
