import os

from dynaconf import Dynaconf

config = Dynaconf(
    envvar_prefix="SAMPLE",
    load_dotenv=True,
    environments=True,
    settings_files=[
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
    ],
)
