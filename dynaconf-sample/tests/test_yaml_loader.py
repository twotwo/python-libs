"""https://github.com/dynaconf/dynaconf/blob/master/tests/test_yaml_loader.py
"""
from __future__ import annotations

import os

import pytest

from dynaconf import LazySettings
from dynaconf.loaders.yaml_loader import load


settings = LazySettings(
    environments=True,
    ENV_FOR_DYNACONF="PRODUCTION",
    ROOT_PATH_FOR_DYNACONF=os.path.dirname(os.path.abspath(__file__)),
)


YAML = """
# the bellow is just to ensure `,` will not break string YAML
default:
  password: 99999
  host: server.com
  port: 8080
  alist:
    - item1
    - item2
    - 23
  service:
    url: service.com
    port: 80
    auth:
      password: qwerty
      test: 1234
development:
  password: 88888
  host: devserver.com
production:
  password: 11111
  host: prodserver.com
global:
  global_value: global
"""

YAML2 = """
global:
  # @float casting not needed, used only for testing
  secret: '@float 42'
  password: 123456
  host: otheryaml.com
"""

YAMLS = [YAML, YAML2]


def test_load_from_yaml():
    """Assert loads from YAML string"""
    load(settings, filename=YAML)
    assert settings.HOST == "prodserver.com"
    assert settings.PORT == 8080
    assert settings.ALIST == ["item1", "item2", 23]
    assert settings.SERVICE["url"] == "service.com"
    assert settings.SERVICE.url == "service.com"
    assert settings.SERVICE.port == 80
    assert settings.SERVICE.auth.password == "qwerty"
    assert settings.SERVICE.auth.test == 1234
    load(settings, filename=YAML, env="DEVELOPMENT")
    assert settings.HOST == "devserver.com"
    load(settings, filename=YAML)
    assert settings.HOST == "prodserver.com"

def test_load_from_multiple_yaml():
    """Assert loads from YAML string"""
    load(settings, filename=YAMLS)
    assert settings.HOST == "otheryaml.com"
    assert settings.PASSWORD == 123456
    assert settings.SECRET == 42.0
    assert settings.PORT == 8080
    assert settings.SERVICE["url"] == "service.com"
    assert settings.SERVICE.url == "service.com"
    assert settings.SERVICE.port == 80
    assert settings.SERVICE.auth.password == "qwerty"
    assert settings.SERVICE.auth.test == 1234
    load(settings, filename=YAMLS, env="DEVELOPMENT")
    assert settings.PORT == 8080
    assert settings.HOST == "otheryaml.com"
    load(settings, filename=YAMLS)
    assert settings.HOST == "otheryaml.com"
    assert settings.PASSWORD == 123456
    load(settings, filename=YAML, env="DEVELOPMENT")
    assert settings.PORT == 8080
    assert settings.HOST == "devserver.com"
    load(settings, filename=YAML)
    assert settings.HOST == "prodserver.com"
    assert settings.PASSWORD == 11111

def test_yaml_key_overriding(tmpdir):
    # export DYNACONF_ALIST='@json ["item1", "item2", "item3", 123]'
    os.environ["DYNACONF_ALIST"] = '@json ["item1", "item2", "item3", 123]'
    tmpfile = tmpdir.mkdir("sub").join("test_yaml_key_overriding.yaml")
    tmpfile.write(YAML)
    config = LazySettings(environments=True, settings_file=str(tmpfile))
    assert config.ALIST == ["item1", "item2", "item3", 123]
