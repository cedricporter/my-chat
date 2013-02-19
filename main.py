#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Hua Liang[Stupid ET] <et@everet.org>
#
import tornado.web
import tornado.ioloop
import os
import logging
import random


logger = logging.getLogger()
 # logger.setLevel(logging.DEBUG)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class TimeMixin(object):
    observers = []
    count = 0
    def register(self, observer):
        cls = TimeMixin
        cls.observers.append(observer)

    def unregister(self, observer):
        cls = TimeMixin
        cls.observers.remove(observer)

    def alert(self):
        cls = TimeMixin
        cls.count += 1
        obs = cls.observers
        cls.observers = []
        for ob in obs:
            ob("Count: %d, Len: %d" % (cls.count, len(obs)))
        print "----- Observer Len: %d -----" % len(obs)


class TimeHandler(tornado.web.RequestHandler, TimeMixin):
    @tornado.web.asynchronous
    def get(self):
         # logger.info("----- register: %d -----" % id(self))
        print "----- register: %d -----" % id(self)
        self.register(self.onMsg)

    def onMsg(self, msg):
        if self.request.connection.stream.closed():
            return
        self.finish(msg)
         # logger.info("----- end %d -----" % id(self))
        print "----- end %d -----" % id(self)

    def on_connection_close(self):
        self.unregister(self.onMsg)


class UpdateTimeHandler(tornado.web.RequestHandler, TimeMixin):
    def get(self):
        self.alert()


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/time", TimeHandler),
    (r"/update", UpdateTimeHandler),
],
debug=True,
template_path=os.path.join(os.path.dirname(__file__), "templates"),
static_path=os.path.join(os.path.dirname(__file__), "static"),
)


if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
