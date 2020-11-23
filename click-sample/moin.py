#!venv/bin/python
# https://click.palletsprojects.com/en/7.x/commands/
import logging
import os
import time
import traceback

import click
from dotenv import find_dotenv, load_dotenv

from util_cli import run

load_dotenv(find_dotenv())


def _remote_action(host, cmd, proxy):
    """
    echo "TS HOST ACTION" >> /tmp/moin.log
    tail -n10 /tmp/moin.log
    """
    # ssh li3huo.com -o "ProxyCommand=nc -X 5 -x 127.0.0.1:1080 %h %p"
    if proxy:
        run(f"ssh {host} -o 'ProxyCommand=nc -X 5 -x 127.0.0.1:1080 %h %p' '{cmd}'")
    else:
        run(f"ssh {host} '{cmd}'")


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option("--proxy/--no-proxy", default=False)
@click.pass_context
def cli(ctx, debug, proxy):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    ctx.obj["PROXY"] = proxy
    # TIMESTAMP
    ctx.obj["TS"] = time.strftime("%Y-%m-%d %H:%M:%S")
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")


@cli.command()
@click.pass_context
@click.option("--host", type=str, envvar="REMOTE_HOST", help="Remote host")
@click.option(
    "--remote", type=str, envvar="REMOTE_DATA", help="Remote path for wiki data"
)
@click.option("--local", envvar="LOCAL_DATA", help="Local path for wiki data")
def pull(ctx, host, remote, local):
    """Pull Remote to Locate"""
    click.secho(f"Action Date: {ctx.obj['TS']}", fg="green")
    click.echo("Debug is %s" % (ctx.obj["DEBUG"] and "on" or "off"))
    click.echo(f"Pull {remote} to {local}")
    _remote_action(host, "tail -n10 /tmp/moin.log", ctx.obj["PROXY"])
    sync_cmd = f'rsync -arvzP --exclude="*/cache" --exclude="*/edit-lock" --exclude="*.swp" --exclude="event-log" --exclude=".DS_Store" --min-size=1 --prune-empty-dirs {remote}/* {local}'
    # run(f"{sync_cmd}:/volume1/algo/model/ct-chest-1mm/{name} {local}/ 2> /dev/null")
    try:
        if click.confirm("rock or not?"):
            # click.echo(click.style("let's rock!", reverse=True, fg="cyan"))
            click.secho("let's rock!", reverse=True, fg="cyan")
            if ctx.obj["PROXY"]:
                run(f"time proxychains4 {sync_cmd}")
            else:
                run(f"time {sync_cmd}")
            _remote_action(
                host,
                f'echo "{ctx.obj["TS"]} {os.getenv("LOCAL_HOST")} PULL" >> /tmp/moin.log',
                ctx.obj["PROXY"],
            )
    except Exception:
        traceback.print_exc()
    click.secho("PULL@" + time.strftime("%Y-%m-%d %H:%M:%S"), reverse=True, fg="cyan")


@cli.command()
@click.pass_context
@click.option("--host", type=str, envvar="REMOTE_HOST", help="Remote host")
@click.option(
    "--remote", type=str, envvar="REMOTE_DATA", help="Remote path for wiki data"
)
@click.option("--local", envvar="LOCAL_DATA", help="Local path for wiki data")
def push(ctx, host, remote, local):
    """Push Locate to Remote"""
    click.secho(f"Action Date: {ctx.obj['TS']}", fg="green")
    click.echo("Debug is %s" % (ctx.obj["DEBUG"] and "on" or "off"))
    click.echo(f"Push {local} to {remote}")
    _remote_action(host, "tail -n10 /tmp/moin.log", ctx.obj["PROXY"])
    sync_cmd = f'rsync -arvzP --exclude="*/cache" --exclude="*/edit-lock" --exclude="*.swp" --exclude="event-log" --exclude=".DS_Store" --min-size=1 --prune-empty-dirs {local}/* {remote}'
    try:
        if click.confirm("rock or not?"):
            if ctx.obj["PROXY"]:
                run(f"time proxychains4 {sync_cmd}")
            else:
                run(f"time {sync_cmd}")
            _remote_action(
                host,
                f'echo "{ctx.obj["TS"]} {os.getenv("LOCAL_HOST")} PUSH" >> /tmp/moin.log',
                ctx.obj["PROXY"],
            )
    except Exception:
        traceback.print_exc()
    click.secho("PUSH@" + time.strftime("%Y-%m-%d %H:%M:%S"), reverse=True, fg="cyan")


if __name__ == "__main__":
    cli(obj={})
