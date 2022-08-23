# README

## Reference

- <https://github.com/Delgan/loguru/>
- <https://loguru.readthedocs.io/en/stable/api/logger.html>

## API

`loguru.logger` 这是 Logger 类的实例，可以把消息分发到当前配置好的 handler 上

- 分发消息： logger.info("hello")
- 设置 handler: logger.add(sink, ...)/logger.remove(sink_id)

一但引入(`import`) `logger`，就可以用来记录程序中发生的信息。不要自己构建 Logger 实例，而是使用 `from loguru import logger`

### logger.add(...)

使用 `add` 方法来处理传入的日志。

sink 是日志最终存放的地方。通过 sink 我们可以传入多种不同的数据结构，汇总如下：

- `sink` 可以传入一个 file 对象，例如 sys.stderr 或者 open('file.log', 'w') 都可以。
- `sink` 可以直接传入一个 str 字符串或者 pathlib.Path 对象，其实就是代表文件路径的，如果识别到是这种类型，它会自动创建对应路径的日志文件并将日志输出进去。
- `sink` 可以是一个方法，可以自行定义输出实现。
- `sink` 可以是一个 logging 模块的 Handler，比如 FileHandler、StreamHandler 等等，或者一个自定义的 Handler。
- `sink` 还可以是一个自定义的类，具体的实现规范可以参见[官方文档](https://loguru.readthedocs.io/en/stable/api/logger.html#sink)。

filter 是用来判断日志是否输出的标志，可以是 `callable`, `str` 或 `dict`：

- `filter` 是函数时，`True` 时会记录日志
- `filter` 是 `str` 时，`record.name` 是 `filter` 或其子类时会记录日志
- `filter` 是 `dict` 时 Value 支持三种格式： `str` / `int` 代表 Logger Level Name; `bool`

## Project Setups

    poetry install
    poetry shell
    pytest test_rotation.py -s

## Use Cases
