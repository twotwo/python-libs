import os
import pprint

from config import config

pp = pprint.PrettyPrinter(indent=1)


def test_config():
    print(f"ENV_FOR_DYNACONF={os.getenv('ENV_FOR_DYNACONF')}")
    print(pp.pformat(config.as_dict()))
    assert config.LOG_LEVEL == "INFO"
    if "dev-81" == os.getenv("ENV_FOR_DYNACONF"):
        assert config.server_ip == "192.168.111.81"
    else:
        # use default value
        assert config.server_ip == "127.0.0.1"
