# python 3 concurrency

[python 3 concurrency](https://docs.python.org/zh-cn/3/library/concurrency.html)

## 进程间通信

### multiprocessing.Pipe([duplex])
返回一对 `Connection` 对象 `(conn1, conn2)` ， 分别表示管道的两端。

如果 duplex 被置为 True (默认值)，那么该管道是双向的。如果 duplex 被置为 False ，那么该管道是单向的，即 conn1 只能用于接收消息，而 conn2 仅能用于发送消息。

### class multiprocessing.Queue([maxsize])
返回一个使用一个管道和少量锁和信号量实现的共享队列实例。当一个进程将一个对象放进队列中时，一个写入线程会启动并将对象从缓冲区写入管道中。

一旦超时，将抛出标准库 queue 模块中常见的异常 queue.Empty 和 queue.Full。

除了 task_done() 和 join() 之外，Queue  实现了标准库类 queue.Queue 中所有的方法。

### class multiprocessing.SimpleQueue
这是一个简化的 Queue 类的实现，很像带锁的 Pipe 。

empty()
如果队列为空返回 True ，否则返回 False 。

get()
从队列中移出并返回一个对象。

put(item)
将 item 放入队列。

### class multiprocessing.JoinableQueue([maxsize])
JoinableQueue 类是 Queue 的子类，额外添加了 task_done() 和 join() 方法。

## Programming guidelines
There are certain guidelines and idioms which should be adhered to when using multiprocessing.
- Avoid shared state
- Picklability
- Thread safety of proxies
- Joining zombie processes
- Better to inherit than pickle/unpickle
- Avoid terminating processes
- Joining processes that use queues
- Explicitly pass resources to child processes
- Beware of replacing sys.stdin with a "file like object"

## 启动并行任务

[concurrent.futures](https://docs.python.org/zh-cn/3/library/concurrent.futures.html) 模块提供异步执行回调高层接口。

异步执行可以由 ThreadPoolExecutor 使用线程或由 ProcessPoolExecutor 使用单独的进程来实现。 两者都是实现抽像类 Executor 定义的接口。

## Sample Code

### multiprocessing basic
[process_test.py](./process_test.py)

### `excutor.py`

### `my-container.py`
