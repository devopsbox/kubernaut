import click
import os


from kubernaut import DEFAULT_CLAIM_NAME


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
    claim_info, kubeconfig_path = kubernaut.claim(name=name, length=length)
    export_message = create_kubeconfig_var_message(str(kubeconfig_path))
    click.echo(export_message)


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
    if "bash" in shell or "zsh" in shell:
        msg += """
        
        export KUBECONFIG={0}
        """
    elif "fish" in shell:
        msg += """ 
        
        set -g -x KUBECONFIG {0}
        """
    elif "csh" in shell:
        msg += """
        
        setenv KUBECONFIG {0}
        """
    else:
        msg += """
        Shell detection failed! Is $SHELL set on this terminal?
        
        If you are using Bash or Zsh then use:
        
        export KUBECONFIG={0}
        
        If you are using Fish then use:
        
        set -g -x KUBECONFIG {0}
        
        If you are using Csh or Tcsh then use:
        
        setenv KUBECONFIG {0}
        
        If you're not using any of these then consult your shell's manual to set $KUBECONFIG to {0}
        """

    return msg.format(path).lstrip()
