#!/usr/bin/env python

import click
import os

from pathlib2 import Path
from scout import Scout

from . import __version__
from . import DEFAULT_REMOTE_API_ADDR
from .claims import commands as claims
from .auth import commands as auth
from .kubernaut import new_kubernaut
from .messages import VERSION_OUTDATED
from urllib.parse import urlparse

PROGRAM_NAME = "kubernaut"

scout = Scout(PROGRAM_NAME, __version__)
scout_result = scout.report()


def create_version_message():
    msg = "%(prog)s v%(version)s"

    latest_version = scout_result.get("latest_version")
    if is_outdated():
        msg += "\n\n" + VERSION_OUTDATED.format(latest_version)

    return msg


def is_outdated():
    latest_version = scout_result.get("latest_version")
    return latest_version != __version__ and not any(v in __version__ for v in ["-"])


@click.group()
@click.version_option(version=__version__, prog_name=PROGRAM_NAME, message=create_version_message())
@click.option(
    "--kubernaut-host",
    envvar="KUBERNAUT_HOST",
    default=DEFAULT_REMOTE_API_ADDR,
    help="Configure remote kubernaut service host (fmt: host:port)",
    type=str
)
@click.pass_context
def cli(ctx, kubernaut_host):
    """kubernaut: easy kubernetes clusters for painless development and testing"""

    use_https = os.getenv("KUBERNAUT_HTTPS", "1") in {"1", "yes", "true"}
    config_root = Path.home() / ".config" / "kubernaut"

    if is_outdated():
        click.echo(VERSION_OUTDATED.format(scout_result.get("latest_version")))

    if not kubernaut_host.startswith("http://") or not kubernaut_host.startswith("https://"):
        scheme = ("https" if use_https else "http")
        kubernaut_host = "{}://{}".format(scheme, kubernaut_host)

    ctx.obj = new_kubernaut(host=urlparse(kubernaut_host), config_root=config_root)


cli.add_command(claims.claim)
cli.add_command(claims.discard)
cli.add_command(claims.get_kubeconfig)
cli.add_command(auth.cli_get_token)
cli.add_command(auth.cli_set_token)
