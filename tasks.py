import time  
from celery import Celery  
import torndb
import json,random

  
# celery = Celery("tasks", broker="amqp://guest:guest@localhost:5672")  
celery = Celery('tasks', broker='amqp://')
# celery.conf.CELERY_RESULT_BACKEND = "amqp"  
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')

db = torndb.Connection('127.0.0.1:3306', 'test_t' , user='root', password='8782') 
 
@celery.task  
def sleep(admin_id):  
	print admin_id
    username = str(random.randint(0,1000))
    sql = 'SELECT id FROM user where username=%s and password=123456' 
    cursor = db.get(sql,username)
    return cursor
  
if __name__ == "__main__":  
    celery.start()  