import tornado
import tornado.process
import tornado.web
from tornado import httpserver
# from tornado import ioloop
from tornado.web import RequestHandler
import json,tornado_mysql,random

import asynctorndb
from tornado_mysql import pools

from tornado import ioloop, gen
import tornado_mysql
# import tornado.wsgi
# import gevent.wsgi
# import pure_tornado


MYSQL_POOL = pools.Pool(dict(host='127.0.0.1', port=3306, user='root', passwd="8782",db='test_t'), max_idle_connections=10, max_open_connections=20)


class non(RequestHandler):
    def get(self):
        """docstring for get"""
        self.write("hello")



class MainHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        username = str(random.randint(0,1000))
        conn = asynctorndb.Connect(user='root', passwd='8782', database='test_t')
        yield conn.connect()
        yield conn.query('SELECT * FROM user where username=username and password=123456')
        # do something with result
        self.write("Hello, world")

class login(tornado.web.RequestHandler):
    # @tornado.web.asynchronous
    @gen.coroutine
   login
        # username = self.get_body_argument('username')
        # password = self.get_body_argument('passwd')
        username = str(random.randint(0,1000))
        password = '123456'

        # conn = yield tornado_mysql.connect("127.0.0.1","root","8782","test_t")
        # cur = conn.cursor()
        # yield cur.execute('SELECT * FROM user where username=username and password=password')
        # print(cur.description)
        # for row in cur:
        #    print(row)
        # cur.close()
        # conn.close()


        cur = yield MYSQL_POOL.execute('SELECT * FROM user where username=username and password=password')
        msg = {'status':'faile'}
        self.write(json.dumps(msg))
        # if not cur.fetchall():
        #     # conn.close()
        #     cur.close()
        #     conn.close()
        #     msg = {'status':'faile'}
        #     self.write(json.dumps(msg))
        # else:
        #     # conn.close()
        #     cur.close()
        #     conn.close()
        #     msg = {'status':'success'}
        #     self.write(json.dumps(msg))

  

application = tornado.web.Application([
    (r"/", non),
    (r"/p", MainHandler),
    (r"/login", login),

])
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


# def main():
#     """docstring for main"""
#     sokets = tornado.netutil.bind_sockets(8080)
#     tornado.process.fork_processes(0)
#     application = tornado.web.Application([
#         ('/',MainHandler),
#         ('/1',non),
#         ('/login',login),
#         ])
#     http_server = httpserver.HTTPServer(application)
#     http_server.add_sockets(sokets)
#     ioloop.IOLoop.instance().start()

# if __name__ == '__main__':
#     main()



