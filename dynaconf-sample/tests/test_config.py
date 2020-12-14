import os
import pprint

from config import config

pp = pprint.PrettyPrinter(indent=1)


def test_config():
    # https://github.com/rochacbruno/dynaconf/blob/master/example/yaml_example/yaml_as_extra_config/app.py
    print(f"ENV_FOR_DYNACONF={os.getenv('ENV_FOR_DYNACONF')}")
    print(f"config={pp.pformat(config.as_dict())}")
    assert config.LOG_LEVEL == "INFO"
    with config.using_env("PRODUCTION"):
        print(f"[PRODUCTION] server_ip={config.server_ip}")
        assert config.server_ip == "127.0.0.1"
    with config.using_env("dev-81"):
        print(f"[dev-81] server_ip={config.server_ip}")
        assert config.server_ip == "192.168.111.81"

    # 有 .env 的时候，环境变量覆盖 config.yaml 中的变量
    if "SAMPLE_LOG_LEVEL" in os.environ:
        print(f"SAMPLE_LOG_LEVEL={os.getenv('SAMPLE_LOG_LEVEL')}")
        assert os.getenv("SAMPLE_LOG_LEVEL") == config.log_level
