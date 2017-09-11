# Tornado-Concurrent-Test
test which method is better for concurrent in tornado
### 分别以多进程（multiple），tornado异步编程（asynchronous），celery的方式测试（ce想要用celery处理数据库io），正常方式（normal）,gevent+multiple process
### 思路
+ 协程
+ 多进程
+ 多进程+协程
+ 减少网络IO
+ 减少数据访问次数，建索引

### 疑惑
+ tornado异步编码方式（用@tornado.web.asynchronous，@tornado.gen.coroutine） 比 不用@@tornado.web.asynchronous，@tornado.gen.coroutine慢
+ 使用 gevent+ tornado（多进程 + 协程 ）性能没有提升？

### 其他

+ 其中还有问题解决ing
