import click
import os


from kubernaut import defaults
from kubernaut import click_utils
from kubernaut.kubernaut_client import KubernautClient
from . import *


@click.command(
    name="claim",
    help="Claim a new Kubernetes cluster"
)
@click.option("--name", default=defaults.DEFAULT_CLAIM_NAME, type=str)
@click.option(
    "--config",
    cls=click_utils.MutuallyExclusiveOption,
    type=click.File(),
    mutually_exclusive=["name"]
)
def claim(name, config):
    config = config or {
        "name": name
    }

    validate_claim_config(config)

    kubernaut = KubernautClient(api_token="foobar")
    click.echo(create_kubeconfig_var_message("/foo/bar"))

    claim_result = kubernaut.claim(**config)


@click.command(
    name="discard",
    help="Discard a previously claimed Kubernetes cluster"
)
@click.option("--name", default=defaults.DEFAULT_CLAIM_NAME, type=str)
def discard(name):
    click.echo("discarding: {}".format(name))


def create_kubeconfig_var_message(path):
    msg = """Set your KUBECONFIG environment variable to use kubectl"""

    shell = os.getenv("SHELL").lower()
    if "/bash" in shell:
        msg += """
        
        export KUBECONFIG={0}
        """
    if "/fish" in shell:
        msg += """ 
        
        set -g -x KUBECONFIG {0}
        """

    return msg.format(path).lstrip()
