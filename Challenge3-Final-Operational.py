#Challenge 3 

#Import libraries for network connectivity, time, ESP32 pin setup, and MQTT communication

import network

import time

import machine

import sys

from umqtt.robust import MQTTClient 

#WiFi Credentials 

ssid = "Digital Native Cyber City"

password = "dncc_wireless"

#MQTT Broker and Client Setup

mqtt_broker = "broker.hivemq.com"

client_id = b"esp32_led_controller_" + machine.unique_id().hex().encode()

#MQTT Topic Setup

control_topic_A = b"wyohack/milk/led/command"

control_topic_B = b"wyohack/milk/led/status"

#MQTT Status Check

print(f"LED Publisher - Client ID: {client_id.decode()}")

print(f"Control Topic: {control_topic_A.decode()}")
      
print(f"Control Topic: {control_topic_B.decode()}")

#Hardware Setup

led_pin_num = 5

led= machine.Pin(led_pin_num, machine.Pin.OUT)

# MQTT Callback Function

def handle_incoming_message(topic, msg):
    command = msg.decode().strip().upper()

    if command == "ON":
        led.on() #LED Is Turned ON
        print("Action: LED Turned On")
        mqtt_client.publish(control_topic_B, b"LED ON") #Publishes LED Status to control_topic_B
    elif command == "OFF":
        led.off() #LED Is Turned OFF
        print("Action: LED Turned OFF")
        mqtt_client.publish(control_topic_B, b"LED OFF") #Publishes LED Status to control_topic_B
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
        print("Netwrok COnfig:", sta_if.ifconfig())
        return True
    else: #All other status's will result in a failure status
        print("!!! WiFi Connection Failed !!!")
        return False 

#Main Execution 

print("--- Starting REPL to MQTT Interaction ---")
wlan = network.WLAN(network.STA_IF)

if connect_wifi(wlan, ssid, password):
    mqtt_client = None
    try:
        # MQTT setup
        mqtt_client = MQTTClient(client_id, mqtt_broker, keepalive=60)
        mqtt_client.set_callback(handle_incoming_message)

        print(f"Connecting to MQTT broker: {mqtt_broker}...")
        mqtt_client.connect()
        print("MQTT Connected!")
        
        #MQTT Subscription

        mqtt_client.subscribe(control_topic_A)
        print(f"Subscribed to '{control_topic_A.decode()}'. Type ON or OFF to publish.\n")

        # Begin IOT Cycle using REPL input 
        while True:
            # 1. Check for incoming MQTT messages
            mqtt_client.check_msg()

            # 2. Wait for REPL input
            command = sys.stdin.readline().strip().upper()
            if command:
                if command in ("ON", "OFF"):
                    msg = command.encode()
                    mqtt_client.publish(control_topic_A, msg)
                    print(f"Published '{command}' to '{control_topic_A.decode()}'")
                else:
                    print(f"Ignored unknown command: '{command}'")
    #Error Checking                    
    except OSError as e:
        print(f"MQTT/Network Error: {e}")
        print("Resetting device in 5 seconds...")
        time.sleep(5)
        machine.reset()
    finally:
        if mqtt_client:
            mqtt_client.disconnect()
        print("MQTT Disconnected. Script finished.")
else:
    print("Cannot start MQTT loop without WiFi.")
                