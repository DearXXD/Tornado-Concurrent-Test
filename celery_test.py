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
from tasks import sleep
import tcelery, tasks  

define("port", default=8000, help="run on the given port", type=int)


tcelery.setup_nonblocking_producer()  

class hello(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello,xiaoxiao')

class SleepHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        # res = yield self.sleep()

        print 1
        # res = yield tornado.gen.Task(tasks.sleep.apply_async)
        sleep.apply_async(args=[1], callback=self.on_success)
        print 2

        # self.write("username %s " % res)
        # self.finish()
        def on_success(self, response):
            # 获取返回的结果
            users = response.result
            self.write(users)
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