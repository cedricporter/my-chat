#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import tornado.web
import tornado.ioloop
import os
import logging
import uuid
from pprint import pprint


logger = logging.getLogger()
# logger.setLevel(logging.INFO)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class TimeMixin(object):
    observers = []
    count = 0
    cache = []

    def register(self, callback, cursor=None):
        print "cursor: ", cursor
        cls = TimeMixin
        if cursor:
            index = 0
            for i in xrange(len(cls.cache)):
                index = len(cls.cache) - i - 1
                if cls.cache[index]["id"] == cursor: break
            recent = cls.cache[index + 1:]
            if recent:
                callback(recent)
                return
        cls.observers.append(callback)

    def unregister(self, callback):
        cls = TimeMixin
        cls.observers.remove(callback)

    def alert(self, message):
        cls = TimeMixin
        cls.cache.extend(message)
        pprint(cls.cache)
        cls.count += 1
        obs = cls.observers
        cls.observers = []
        for cb in obs:
            cb(message)
        print "----- Observer Len: %d -----" % len(obs)


class TimeHandler(tornado.web.RequestHandler, TimeMixin):
    @tornado.web.asynchronous
    def post(self):
        cursor = self.get_argument("cursor", None)
        print "----- register: %d -----" % id(self)
        self.register(self.onMsg,
                      cursor=cursor)

    def onMsg(self, msg):
        if self.request.connection.stream.closed():
            return
        self.finish(dict(messages=msg))
        print "----- end %d -----" % id(self)

    def on_connection_close(self):
        self.unregister(self.onMsg)


class UpdateTimeHandler(tornado.web.RequestHandler, TimeMixin):
    def get(self):
        self.alert()

    def post(self):
        from pprint import pprint

        message = {
            "id": str(uuid.uuid4()),
            "from": "user",
            "body": self.get_argument("body"),
        }
        message["html"] = "<div>%s</div>" % message["body"]

        pprint(message)

        self.alert([message])

        self.write(message)


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
