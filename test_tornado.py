import tornado.ioloop
import tornado.web
import json,tornado_mysql,random

import tornado.gen
from tornado_mysql import pools
import MySQLdb

MYSQL_POOL = pools.Pool(dict(host='127.0.0.1', port=3306, user='root', passwd="8782",db='test_t'), max_idle_connections=10, max_open_connections=20)

class Handler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
 
        cur = yield MYSQL_POOL.execute('SELECT * FROM table_1 LIMIT 1')
  
        self.write('ok')
        self.finish()



def get_conn():
    db = MySQLdb.connect("127.0.0.1","root","8782","test_t")
    #db.autocommit(False)
    return db

def query(db):
    cursor=db.cursor()
    cursor.execute("select * from user ")
    result=cursor.fetchall()
    cursor.close()
    if result:
        return result

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        db=get_conn()
        rs = query(db)
        print(rs)
        # db.close()
        self.write("Hello, world%s"%list(rs))

class hello(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write('Hello,xiaoxiao')
        self.finish()

class add(tornado.web.RequestHandler):
    def post(self):
        res = Add(json.loads(self.request.body))
        self.write(json.dumps(res))

class regist(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self,*args ,**kwargs):
        username = self.get_body_argument('username')
        passwd = self.get_body_argument('passwd')
        # conn =  tornado_mysql.connect(host='127.0.0.1', port=3306, user='root', passwd="8782",db='test_t')
        # cur = conn.cursor()
        # try:
        users = xrange(int(username))
        for i in users:
            cur = yield MYSQL_POOL.execute("insert into user (username,password) values (%s,%s)",(i, passwd))
    
            print dir(cur)
        # except Exception , e:
        #     yield cur.rollback()  
        #     print str(e) 
        # yield MYSQL_POOL.commit()
        msg = {'status':'success1'}
        self.write(json.dumps(msg))




class login(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args ,**kwargs):
        # username = self.get_body_argument('username')
        # password = self.get_body_argument('passwd')
        username = str(random.randint(0,1000))
        password = '123456'
        # conn = tornado_mysql.connect(host='127.0.0.1', port=3306, user='root', passwd="8782",db='test_t')


        # cur = conn.cursor()
        cur = yield MYSQL_POOL.execute('SELECT * FROM user where username=username and password=password')
        if not cur.fetchall():
            msg = {'status':'faile'}
            self.write(json.dumps(msg))
        else:
            msg = {'status':'success'}
            self.write(json.dumps(msg))

def Add(input):
    sum = input['num1'] + input['num2']
    result = {}
    result['sum'] = sum
    return result

application = tornado.web.Application([
    (r"/", hello),
    (r"/add", add),
    (r"/p", MainHandler),
    (r"/login", login),
    (r"/regist", regist),

])
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()