import tornado.ioloop
import tornado.web
import MySQLdb

def get_conn():
    db = MySQLdb.connect("127.0.0.1","root","8782","communityshare")
    #db.autocommit(False)
    return db

def query(db):
    cursor=db.cursor()
    cursor.execute("select * from accounts_user where id = 1")
    result=cursor.fetchall()
    cursor.close()
    if result:
        return result

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        db=get_conn()
        query(db)
        db.close()
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/d", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()