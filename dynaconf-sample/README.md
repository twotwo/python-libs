# dynaconf-sample

Injection configuration information with Dynaconf.

Apply `Dependency Inversion Principle` and make model easy to test.

[Dynaconf Quick Start](https://www.dynaconf.com)

## Dependency

```bash
$ poetry show --tree --no-dev
dynaconf 3.1.2 The dynamic configurator for your Python Project
```

## Installation

```bash
# create virtual env
$ virtualenv venv -p python3 && source venv/bin/activate
$ pip install --upgrade pip && \
  pip install -r requirements.txt && \
  pip install -r requirements-dev.txt
```

## Running on host

1. config.yaml - 配置多套环境参数
2. .env - 在环境变量中指定使用哪一套参数
3. config.py - 应用如何加载 `config.yaml`
4. test_config.py - 如何获取配置参数

```bash
# unit test
$ export PYTHONPATH=.
$ pytest
```
