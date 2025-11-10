#Challenge 3 

#Import libraries for network connectivity, time, ESP32 pin setup, and MQTT communication

import network 

import time

import machine

from umqtt.robust import MQTTClient 

#WiFi Credentials 

ssid = "Omitted"

password = "Omitted"

#MQTT Broker and Client Setup

mqtt_broker = "broker.hivemq.com"

client_id_A = b"esp32_led_controller_” + machine.unique_id()

#MQTT Topic Setup

control_topic_A = b"wyohack/milk/led/command”

control_topic_B = b"wyohack/milk/led/status”

#MQTT Status Check

print(f"LED Publisher - Client ID: {client_id_A.decode()}")

print(f"Control Topic: {control_topic_A.decode()}")
      
print(f"Control Topic: {control_topic_B.decode()}")

#Hardware Setup

led_pin_num = 25 

led= machine.Pin(led_pin_num, machine.Pin.OUT)

# MQTT Callback Function

if command == "ON":
    led.on() #LED Is Turned ON
elif command == "OFF":
    led.off() #LED Is Turned OFF
    print("Action:LED Turned OFF")
else:
    print(f"Action: Unkown command '{command}' ignored.") #Ignores all else

#WiFi Connection 

def connect_wifi(sta_if, ssid, password): #Specifies variables used in connection
    print(f"Connecting to WiFi network: {ssid}...") #Prints connection status with ssid
    if not sta_if.isconnected(): #If the interface is not active, it will attempt to activate and connect
        sta_if.active(True)
        sta_if.connect(ssid, password)
        max_wait = 15
        while not sta_if.isconnected() and max_wait > 0:
            print(".", end="")
            time.sleep(1)
            max_wait -= 1
        print()
    if sta_if.isconnected(): #If the interface is active and WiFi is connected, a positive status will be printed
        print("WiFi Connection Successful!")
        print("Netwrok COnfig:", staf_if.ifconfig())
        return True
    else: #All other status's will result in a failure status
        print("!!! WiFi Connection Failed !!!")
        return False 
    
          
