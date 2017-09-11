
import torndb
import random
from tornado.options import define, options
import tornado.process
import tornado.web
from tornado import httpserver
# from tornado import ioloop
from tornado.web import RequestHandler

# db = torndb.Connection(host='127.0.0.1', port=3306, user='root', passwd="8782",db='test_t') 

class login(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        username = str(random.randint(0,1000))
        sql = 'SELECT id FROM user where username=%s and password=123456' 
        cursor = self.application.db.get(sql,username)
        self.write(cursor)



class CustomApplication(tornado.web.Application):
    def __init__(self):
        handles = [
            (r'/login',login),
        ]
        super(CustomApplication, self).__init__(handles)
        self.db = torndb.Connection('127.0.0.1:3306', 'test_t' , user='root', password='8782')


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(CustomApplication())
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()