# README

## Loguru Docs

- <https://loguru.readthedocs.io/en/stable/api/logger.html>
- [使用loguru记录日志](https://www.jianshu.com/p/2945634fe349)

### API 概述

`loguru.logger` 这是 Logger 类的实例，可以把消息分发到当前配置好的 handler 上

- 分发消息： logger.info("hello")
- 设置 handler: logger.add(sink, ...)/logger.remove(sink_id)

sink 是其中非常重要的一个概念。通过 sink 我们可以传入多种不同的数据结构，汇总如下：

- `sink` 可以传入一个 file 对象，例如 sys.stderr 或者 open('file.log', 'w') 都可以。
- `sink` 可以直接传入一个 str 字符串或者 pathlib.Path 对象，其实就是代表文件路径的，如果识别到是这种类型，它会自动创建对应路径的日志文件并将日志输出进去。
- `sink` 可以是一个方法，可以自行定义输出实现。
- `sink` 可以是一个 logging 模块的 Handler，比如 FileHandler、StreamHandler 等等，或者一个自定义的 Handler。
- `sink` 还可以是一个自定义的类，具体的实现规范可以参见[官方文档](https://loguru.readthedocs.io/en/stable/api/logger.html#sink)。

## Project Setups

    poetry install
    poetry shell

## Unit Test

    pytest test_rotation.py -s
