import torndb
import random
import tornado.web
# db = torndb.Connection(host='127.0.0.1', port=3306, user='root', passwd="8782",db='test_t') 

class login(tornado.web.RequestHandler):
	def get(self):
		username = str(random.randint(0,1000))
		sql =   'SELECT id FROM user where username=%s and password=123456' 
		if self.application.db.get(sql,username):
			self.write({'status':'success'})
		else:
			self.write({'status': 'no'})

class CustomApplication(tornado.web.Application):
	def __init__(self):
		handles = [
			(r'/login',login),
		]
		super(CustomApplication, self).__init__(handles)
		self.db = torndb.Connection('127.0.0.1:3306', 'test_t' , user='root', password='8782') 


if __name__ == "__main__":
    sokets = tornado.netutil.bind_sockets(8080)
    tornado.process.fork_processes(0)
    http_server = tornado.httpserver.HTTPServer(CustomApplication())
    http_server.add_sockets(sokets)
    tornado.ioloop.IOLoop.instance().start()