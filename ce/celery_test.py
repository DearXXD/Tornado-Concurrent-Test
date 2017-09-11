# -*- coding:utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json,tornado_mysql,random
import asynctorndb
import torndb
import tornado.gen
from tornado.options import define, options

import tcelery, tasks  
from tasks import sleep

define("port", default=8000, help="run on the given port", type=int)


tcelery.setup_nonblocking_producer()  

class hello(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello,xiaoxiao')

class SleepHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        sleep.apply_async(args=[1],callback=self.on_result)
        # res = yield tornado.gen.Task(tasks.sleep.apply_async, args=[self.application.db])
        self.write("username %s " % 123)
        self.finish()

    def on_result(self, response):
        self.write(str(response.result))
        self.finish()

class CustomApplication(tornado.web.Application):
    def __init__(self):
        handles = [
            (r"/sleep", SleepHandler),
            (r'/hello',hello),
        ]
        super(CustomApplication, self).__init__(handles)
        self.db = torndb.Connection('127.0.0.1:3306', 'test_t' , user='root', password='8782') 


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(CustomApplication())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()