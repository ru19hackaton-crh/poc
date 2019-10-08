#!/usr/bin/env python3

import logging
from tornado import websocket
import tornado.ioloop
from tornado.log import enable_pretty_logging
enable_pretty_logging()


class CommonBrainHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("Websocket Opened")

    def on_close(self):
        logging.info("Websocket closed")

class MonitorHandler(CommonBrainHandler):
    def on_message(self, message):
        self.write_message(u"Monitor said: %s" % message)

class RobotHandler(CommonBrainHandler):
    def on_message(self, message):
        self.write_message(u"Robot said: %s" % message)

application = tornado.web.Application([
    (r"/monitor", MonitorHandler),
    (r"/robot", RobotHandler),
    ])

if __name__ == "__main__":
    application.listen(9000)
    tornado.ioloop.IOLoop.current().start()
