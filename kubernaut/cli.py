#!/usr/bin/env python

import click
import os

from scout import Scout

from . import __version__
from . import DEFAULT_REMOTE_API_ADDR
from .claims import commands as claims
from .auth import commands as auth
from .kubernaut import new_kubernaut
from urllib.parse import urlparse, urlsplit

PROGRAM_NAME = "kubernaut"

scout = Scout(PROGRAM_NAME, __version__)
scout_result = scout.report()


VERSION_OUTDATED_MSG = "Your version of %(prog)s is out of date! The latest version is {0}." + \
                       " Please go to " + click.style("https://github.com/datawire/kubernaut", underline=True) + \
                       " for update instructions."


def create_version_message():
    msg = "%(prog)s v%(version)s"

    latest_version = scout_result.get("latest_version")
    if is_outdated():
        msg += "\n\n" + VERSION_OUTDATED_MSG.format(latest_version)

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

    use_https = os.getenv("KUBERNAUT_HTTPS", "1") in {1, "yes", "true"}

    if is_outdated():
        click.echo(VERSION_OUTDATED_MSG.format(scout_result.get("latest_version")))

    if not kubernaut_host.startswith("http://") or not kubernaut_host.startswith("https://"):
        scheme = ("https" if use_https else "http")
        kubernaut_host = "{}://{}".format(scheme, kubernaut_host)

    ctx.obj = new_kubernaut(urlparse(kubernaut_host))


cli.add_command(claims.claim)
cli.add_command(claims.discard)
cli.add_command(auth.cli_get_token)
cli.add_command(auth.cli_set_token)
