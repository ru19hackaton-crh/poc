#!/usr/bin/env python3

from tornado import websocket
import tornado.ioloop


class CommonBrainHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("Websocket Opened")

    def on_close(self):
        print("Websocket closed")

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
