#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

import asyncio
import websockets


async def hello():
    uri = "ws://localhost:1234"
    async with websockets.connect(uri) as websocket:
        name = "Crazy Robot Hackers"

        await websocket.send(name)
        print("> %s" % name)

        greeting = await websocket.recv()
        print("< %s" % greeting)

if __name__ == "__main__":
    print("hello from robot")

    asyncio.get_event_loop().run_until_complete(hello())
