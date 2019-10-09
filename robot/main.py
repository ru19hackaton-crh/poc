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

async def read_messages():
    url = "ws://localhost:9000/robot"
    conn = await websocket_connect(url)
    while True:
        msg = await conn.read_message()
        if msg is None: break
        # Do something with msg
        logging.info("< %s" % msg)

def run_logic():
    logging.info("Logic time!")

if __name__ == "__main__":
    logging.info("hello from robot")

    logic = tornado.ioloop.PeriodicCallback(run_logic, 1000)
    tornado.ioloop.IOLoop.current().spawn_callback(read_messages)
    logic.start()
    tornado.ioloop.IOLoop.current().start()
