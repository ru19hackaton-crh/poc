#!/usr/bin/env python3
import logging

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

from tornado.websocket import websocket_connect
import tornado.ioloop
from tornado.log import enable_pretty_logging
enable_pretty_logging()

import json

class Logic:

    def __init__(self):
        self.current = None

    async def read_messages(self):
        url = "ws://localhost:9000/robot"
        conn = await websocket_connect(url)
        while True:
            msg = await conn.read_message()
            if msg is None: break
            if msg.startswith("COMMAND:"):
                command = msg.replace("COMMAND: ", "")
                self.current = command

    def run(self):
        logging.info("# %s" % self.current)

if __name__ == "__main__":
    logging.info("hello from robot")

    logic = Logic()
    logic_processing = tornado.ioloop.PeriodicCallback(logic.run, 1000)
    tornado.ioloop.IOLoop.current().spawn_callback(logic.read_messages)
    logic_processing.start()
    tornado.ioloop.IOLoop.current().start()
