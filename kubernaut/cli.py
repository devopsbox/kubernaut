#!/usr/bin/env python

import click
import platform
from . import __version__
from scout import Scout

from os import getenv
from sys import exit

from .claims import commands as claims
from .auth import commands as auth

from .kubernaut import new_kubernaut

# ----------------------------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------------------------

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

PROGRAM_NAME = "kubernaut"

KUBERNAUT_HTTPS = getenv("KUBERNAUT_HTTPS", "1").lower() in {"1", "true", "yes"}
KUBERNAUT_HOST = getenv("KUBERNAUT_HOST", "kubernaut.io")
KUBERNAUT_ADDR = ("https://{0}" if KUBERNAUT_HTTPS else "http://{0}").format(KUBERNAUT_HOST)


scout = Scout(PROGRAM_NAME, __version__)
scout_result = scout.report()

# Formatting Notes
# ----------------
#
# %(prog)s is interpreted by the click library.
# {0}      is interpreted by kubernaut itself to inject version information.
#
VERSION_OUTDATED_MSG = "Your version of %(prog)s is out of date! The latest version is {0}." + \
                       " Please go to " + click.style("https://github.com/datawire/kubernaut", underline=True) + \
                       " for update instructions."

LOGIN_MSG = click.style("Kubernaut is a free service! Please get an access token to use Kubernaut => ") + \
            click.style("https://kubernaut.io/token", bold=True, underline=True) + "\n\n" + \
            click.style("Once you have your token please run `kubernaut set-token <TOKEN>`")

USER_AGENT = "{0}/{1} ({2}; {3})".format(PROGRAM_NAME, __version__, platform.system(), platform.release())

CLAIM_LIMITATION_MSGS = [
    click.style("Warning: ", fg="yellow", bold=True) + click.style("Kubernaut does not currently support LoadBalancer services!")
]


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
    default="kubernaut.io",
    help="Configure remote kubernaut service host",
    type=str
)
@click.pass_context
def cli(ctx, kubernaut_host):
    """kubernaut: easy kubernetes clusters for painless development and testing"""

    if is_outdated():
        click.echo(VERSION_OUTDATED_MSG.format(scout_result.get("latest_version")))

    ctx.obj = new_kubernaut(kubernaut_host)


cli.add_command(claims.claim)
cli.add_command(claims.discard)
cli.add_command(auth.cli_get_token)
cli.add_command(auth.cli_set_token)
