from models import *
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client
import random
import dht11
import os
from asyncio_mqtt import Client, MqttError
import time
import asyncio
from decimal import Decimal

global moisture_val
moisture_val = 0

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setup(18, GPIO.OUT) # Relay 1
    GPIO.setup(22, GPIO.OUT) # Relay 2
    GPIO.setup(23, GPIO.OUT) # RED led
    GPIO.setup(24, GPIO.OUT) # BLUE led
    GPIO.setup(17, GPIO.OUT) # LDR Out
    GPIO.setup(27, GPIO.OUT) # LDR IN

def read_ldr(mpin,tpin):
    cap=0.00000001
    adj=2.5
    i=0
    t=0
    while True:
        GPIO.setup(mpin, GPIO.OUT)
        GPIO.setup(tpin, GPIO.OUT)
        GPIO.output(mpin, False)
        GPIO.output(tpin, False)
        time.sleep(0.2)
        GPIO.setup(mpin, GPIO.IN)
        time.sleep(0.2)
        GPIO.output(tpin, True)
        start_time=time.time()
        end_time=time.time()
        while (GPIO.input(mpin) == GPIO.LOW):
            end_time=time.time()
        res_val=end_time-start_time
        res=(res_val/cap)*adj
        i=i+1
        t=t+res
        if i==10:
            t=t/i
            t=t/100000
            cur_light = round(Decimal(10-t),2)
            t=0
            i=0
            return cur_light

def read_dht(instance):
    result = instance.read()
    if result.is_valid():
        cur_temp = result.temperature
        cur_humid = result.humidity
        return (cur_temp,cur_humid)
    else:
        print("DHT11 Readings Invalid.")
        print(result)
        return (-1,-1)

def fetch_configs():
    max_temp = eval(Configs.filter(Configs.name == 'max_temp').first().value)
    max_light = eval(Configs.filter(Configs.name == 'max_light').first().value)
    return (max_temp,max_light)

async def connect_mqtt():
    async with Client("localhost") as client:
        async with client.filtered_messages("/piplanter/moisture") as messages:
            await client.subscribe("/piplanter/moisture")
            async for message in messages:
                handle_moisture(message.payload.decode())

def fetch_moisture():
    moisture = eval(Sensor.filter(Sensor.name == 'moisture').first().value)
    return moisture

async def main():
    init()
    dht = dht11.DHT11(pin=4)
    try:
        while True:
            (temperature,humidity) = read_dht(dht)
            print(f"Temperature: {temperature}")
            print(f"Humidity: {humidity}")
            Sensor.replace(name='temperature',value=temperature).execute()
            Sensor.replace(name='humidity',value=humidity).execute()
            light = read_ldr(26,21) # LDR Pins
            Sensor.replace(name='light',value=light).execute()
            print(f"Light: {light}")
            (max_temp,max_light) = fetch_configs()
            moisture_val = fetch_moisture()
            print(f"Moisture: {moisture_val}")
            if(light>int(max_light) or temperature>int(max_temp)):
                GPIO.output(18, 1)
                GPIO.output(22, 1)
                GPIO.output(23, 1)
                time.sleep(1)
                GPIO.output(23, 0)
                time.sleep(1)
                print("Alert!! Values Greater!")
            elif(light<=int(max_light) and temperature<=int(max_temp)):
                print("Values Fine")
                if int(moisture_val)<400:
                    GPIO.output(23, 1)
                    GPIO.output(24, 0)
                    print("Watering...")
                    GPIO.output(18, 0)
                    GPIO.output(22, 0)
                elif int(moisture_val)>=400:
                    GPIO.output(23, 0)
                    GPIO.output(24, 1)
                    print("Its Wet!")
                    GPIO.output(18, 1)
                    GPIO.output(22, 1)
            else:
                print("Error in Comparison")
            time.sleep(5)
    except Exception as e:
        GPIO.cleanup()
        print("Exception: ")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())