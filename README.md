# Tornado-Concurrent-Test
test which method is better for concurrent in tornado
### 分别以多进程（multiple），tornado异步方式（asynchronous），celery的方式测试（ce，想要用celery处理数据库io），正常方式（normal）,gevent+multiple process（test_gevent）
### 思路
+ 协程  （@tornado.gen.coroutine，gevent）
+ 多进程
+ 多进程+协程 
+ 减少网络IO
+ 减少数据访问次数，建索引

### 疑惑
+ tornado异步编码方式（用@tornado.web.asynchronous，@tornado.gen.coroutine） 比 不用(@tornado.web.asynchronous，@tornado.gen.coroutine) 慢? 使用方式不对？ 待排查？
+ 使用 gevent+ tornado（多进程 + 协程 ）性能没有提升？
+ 使用异步 @tornado.web.asynchronous or 协程 @tornado.gen.coroutine 方式， mysql出错（Commands out of sync; you can't run this command now， mysql连接？）

### 其他

+ 其中还有问题解决ing
