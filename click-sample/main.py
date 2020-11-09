#!venv/bin/python
# https://click.palletsprojects.com/en/7.x/commands/
import traceback
import logging
import click

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")


@cli.command()
@click.pass_context
@click.option("--path", type=str, envvar="REMOTE_DATA", help="Remote path for wiki data")
@click.option("--limit", default=100, help="Max count to list")
def moin_pull(ctx, path, limit):
    """Show dicom info in path"""
    click.echo("Debug is %s" % (ctx.obj["DEBUG"] and "on" or "off"))
    click.echo(f"Show dicom info in path: {path}, limit={limit}")
    try:
        if click.confirm("rock or not?"):
            # click.echo(click.style("let's rock!", reverse=True, fg="cyan"))
            click.secho("let's rock!", reverse=True, fg="cyan")
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    cli(obj={})
