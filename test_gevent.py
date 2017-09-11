# encoding: utf-8

from gevent import monkey
monkey.patch_all()

import functools
import random
import gevent
import tornado.ioloop
import tornado.web
import tornado.httpserver
import torndb



class hello(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello,xiaoxiao')

#同步测试
def se(db):
    username = str(random.randint(0, 1000))
    sql = 'SELECT id FROM user where username=%s and password=123456'
    res = db.get(sql, username)

class LoHandler(tornado.web.RequestHandler):

    def get(self):
        a = gevent.spawn(se,self.application.db)
        print dir(a)
        print a.value
        self.write("Done")


from tornado.concurrent import Future

# Asynchronous decorator
def gfuture(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        loop = tornado.ioloop.IOLoop.current()
        future = Future()

        def call_method():
            try:
                result = func(*args, **kwargs)
                loop.add_callback(functools.partial(future.set_result, result))
            except Exception, e:
                loop.add_callback(functools.partial(future.set_exception, e))
        gevent.spawn(call_method)
        return future
    return f

@gfuture
def gfetch(db):
    username = str(random.randint(0, 1000))
    sql = 'SELECT id FROM user where username=%s and password=123456'
    res = db.get(sql, username)
    return res

class LoginHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        n = yield gfetch(self.application.db)
        self.write("success %s" % n)

class CustomApplication(tornado.web.Application):
    def __init__(self):
        handles = [
            (r"/login", LoginHandler),
            (r'/hello',hello),
            (r'/l', LoHandler),
        ]
        super(CustomApplication, self).__init__(handles)
        self.db = torndb.Connection('127.0.0.1:3306', 'test_t' , user='root', password='8782')

if __name__ == "__main__":
    sokets = tornado.netutil.bind_sockets(9998)
    tornado.process.fork_processes(0)
    http_server = tornado.httpserver.HTTPServer(CustomApplication())
    http_server.add_sockets(sokets)
    tornado.ioloop.IOLoop.instance().start()
