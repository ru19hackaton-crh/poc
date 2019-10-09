#!/usr/bin/env python3

import py_trees
from py_trees.blackboard import BlackboardClient
from py_trees.common import Status

import logging
from tornado import websocket
import tornado.ioloop
from tornado.log import enable_pretty_logging
enable_pretty_logging()

class ManualDriveBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Manual Drive"):
        super().__init__(name)
        self.blackboard.register_key("manual", read=True)
        self.blackboard.register_key("keys", read=True)

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        if self.blackboard.manual:
            if self.status != Status.RUNNING:
                # inform robot that manual is on
                self.brain.robot.write_message(f"manual: True")
            self.brain.robot.write_message(f"keys: {self.blackboard.keys}")
            return Status.RUNNING
        elif self.status == Status.RUNNING:
            # inform robot that manual is off
            self.brain.robot.write_message(f"manual: False")
            return Status.SUCCESS
        else:
            return py_trees.common.Status.INVALID

    def terminate(self, new_status):
        pass

def create_tree(brain):
    root = py_trees.composites.Selector(name="POC root")
    manual = ManualDriveBehaviour()
    manual.setup(0, brain)
    root.add_children([manual])
    return root

class Brain:
    def __init__(self):
        self._monitor = None
        self._robot = None

        self.tree = create_tree(self)
        self.behaviour_tree = py_trees.trees.BehaviourTree(self.tree)

        self.bb = BlackboardClient(name="Brain", write={"manual", "keys"})
        self.bb.manual = False
        self.bb.keys = set()

    def operate(self):
        py_trees.blackboard.Blackboard.enable_activity_stream(maximum_size=100)
        self.behaviour_tree.tick()
        logging.info(py_trees.display.ascii_tree(self.tree, show_status=True))
        logging.info(py_trees.display.unicode_blackboard_activity_stream())
        py_trees.blackboard.Blackboard.activity_stream.clear()

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

    @property
    def manual(self):
        return self.bb.manual
    @manual.setter
    def manual(self, state):
        self.bb.manual = state

    def parse_robot(self, message):
        self.robot.write_message(u"Robot said: %s" % message)

    def parse_monitor(self, message):
        if message == "manual on":
            self.manual = True
        elif message == "manual off":
            self.manual = False
        elif message.endswith("up"):
            key = message.split(" ")[0]
            self.bb.keys.remove(key)
        elif message.endswith("down"):
            key = message.split(" ")[0]
            self.bb.keys.add(key)
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
