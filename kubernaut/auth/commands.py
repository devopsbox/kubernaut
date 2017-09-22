import click


@click.command(
    name="get-token",
    help="Get an authentication token"
)
def cli_get_token():
    msg = click.style("Kubernaut is a free service! Please get an access token to use Kubernaut\n\n")
    msg += click.style("https://kubernaut.io/token", bold=True, underline=True)
    msg += click.style("\n\nAfterwards run `kubernaut set-token <TOKEN>`")

    click.echo(msg)


@click.command(
    name="set-token",
    help="Set an authentication token"
)
@click.argument("token")
@click.pass_obj
def cli_set_token(kubernaut, token):
    kubernaut.update_config("token", token)
