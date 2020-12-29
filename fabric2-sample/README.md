# fabric2-sample

use fabric v2 to execute shell commands remotely over SSH.

[Tutorial](https://docs.fabfile.org/en/2.5/getting-started.html#addendum-the-fab-command-line-tool)

## Running on host

```bash
# create virtual env
$ virtualenv venv -p python3 && source venv/bin/activate
$ pip install --upgrade pip && \
  pip install -r requirements.txt && \
  pip install -r requirements-dev.txt
```

[Command-line interface](https://docs.fabfile.org/en/2.5/cli.html)

```bash
# running command
$ fab --list
$ fab -H dev.gpu install-zsh
```

[Configuration](https://docs.fabfile.org/en/2.5/concepts/configuration.html) ./fabric.yaml

```yaml
connect_kwargs:
  password: welcome-to-heaven
sudo:
  password: welcome-to-heaven
timeouts: 
  connect: 10
user: god
port: 22
```
