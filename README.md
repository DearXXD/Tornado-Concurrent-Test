# Tornado-Concurrent-Test
test which method is better for concurrent in tornado
+ 分别以多进程（multiple），tornado异步编程（asynchronous），celery的方式测试（ce想要用celery处理数据库io），正常方式（normal）

+ 减少网络IO
+ 减少数据访问次数，建索引
+ 协程
+ 其中还有问题解决ing
