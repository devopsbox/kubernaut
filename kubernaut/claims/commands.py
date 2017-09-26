import click
import re
import os


from kubernaut import DEFAULT_CLAIM_NAME
from kubernaut.kubernaut import KubernautServiceException


@click.command(
    name="claim",
    help="Claim a new Kubernetes cluster"
)
@click.option(
    "--name",
    default=DEFAULT_CLAIM_NAME,
    help="Name of the claim",
    type=str
)
@click.option(
    "--length",
    default=6,
    help="Length (in hours) that the claim will exist before being expired",
    type=int
)
@click.pass_obj
def claim(kubernaut, name, length):
    try:
        claim_info, kubeconfig_path = kubernaut.claim(name=name, length=length)
        export_message = create_kubeconfig_var_message(str(kubeconfig_path))
        click.echo(export_message)
    except KubernautServiceException as e:
        exit(1)


@click.command(
    name="discard",
    help="Discard a claimed Kubernetes cluster"
)
@click.option("--name", default=DEFAULT_CLAIM_NAME, type=str)
@click.pass_obj
def discard(kubernaut, name):
    kubernaut.discard(name=name)


def create_kubeconfig_var_message(path):
    msg = """Set your KUBECONFIG environment variable to use kubectl"""

    shell = os.getenv("SHELL").lower()
    if "/bash" in shell or "/zsh" in shell:
        msg += """
        
        export KUBECONFIG={0}
        """
    if "/fish" in shell:
        msg += """ 
        
        set -g -x KUBECONFIG {0}
        """

    return msg.format(path).lstrip()
