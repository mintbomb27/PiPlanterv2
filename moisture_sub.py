from models import *
from asyncio_mqtt import Client
import asyncio

def handle_moisture(moisture_val):
    print(f"Moisture Received: {moisture_val}")
    moisture = (Sensor.replace(name='moisture',value=moisture_val).execute())

async def subscribe():
    async with Client("localhost") as client:
        async with client.filtered_messages("/piplanter/moisture") as messages:
            await client.subscribe("/piplanter/moisture")
            async for message in messages:
                handle_moisture(message.payload.decode())

asyncio.run(subscribe())