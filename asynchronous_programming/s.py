# -*- coding:utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import random
import torndb
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

class hello(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello,xiaoxiao')

executor = ThreadPoolExecutor(10)

# db = torndb.Connection('127.0.0.1:3306', 'test_t', user='root', password='8782')

def search(db):
    username = str(random.randint(0, 1000))
    sql = 'SELECT id FROM user where username=%s and password=123456'
    cursor = db.get(sql, username)
    return cursor['id']

class LoginHandler(tornado.web.RequestHandler):

    # @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):

        res = yield  executor.submit( search,self.application.db)
        self.write("success! username %s " %res )
        # self.finish()

class CustomApplication(tornado.web.Application):
    def __init__(self):
        handles = [
            (r"/login", LoginHandler),
            (r'/hello',hello),
        ]
        super(CustomApplication, self).__init__(handles)
        self.db = torndb.Connection('127.0.0.1:3306', 'test_t' , user='root', password='8782')

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(CustomApplication())
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
