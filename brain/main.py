#!/usr/bin/env python3

import logging
from tornado import websocket
import tornado.ioloop
from tornado.log import enable_pretty_logging
enable_pretty_logging()

class Brain:
    def __init__(self):
        self._monitor = None
        self._robot = None

    def operate(self):
        # brain loop
        #logging.info("foo")
        return

    @property
    def monitor(self):
        return self._monitor
    @monitor.setter
    def monitor(self, monitor):
        self._monitor = monitor
        logging.info("new monitor set")

    @property
    def robot(self):
        return self._robot
    @robot.setter
    def robot(self, robot):
        self._robot = robot
        logging.info("new robot set")

    def parse_robot(self, message):
        self.robot.write_message(u"Robot said: %s" % message)

    def parse_monitor(self, message):
        if message == "manual on":
            logging.info("setting manual on")
        elif message == "manual off":
            logging.info("setting manual off")
        else:
            self.monitor.write_message(f"message: {message}")
        return

class CommonBrainHandler(websocket.WebSocketHandler):

    def initialize(self, brain):
        self.brain = brain

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("Websocket Opened")

    def on_close(self):
        logging.info("Websocket closed")

class MonitorHandler(CommonBrainHandler):
    def open(self):
        self.brain.monitor = self

    def on_message(self, message):
        self.brain.parse_monitor(message)

class RobotHandler(CommonBrainHandler):
    def open(self):
        self.brain.robot = self

    def on_message(self, message):
        self.brain.parse_robot(message)


if __name__ == "__main__":
    brain = Brain()

    brain_operating = tornado.ioloop.PeriodicCallback(brain.operate, 1000)
    application = tornado.web.Application([
        (r"/monitor", MonitorHandler, dict(brain=brain)),
        (r"/robot", RobotHandler, dict(brain=brain)),
        ])
    application.listen(9000)

    brain_operating.start()
    tornado.ioloop.IOLoop.current().start()
