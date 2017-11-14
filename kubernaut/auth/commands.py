import click

from kubernaut.messages import GET_TOKEN


@click.command(
    name="get-token",
    help="Get an authentication token"
)
def cli_get_token() -> None:
    click.echo(GET_TOKEN)


@click.command(
    name="set-token",
    help="Set an authentication token"
)
@click.argument("token")
@click.pass_obj
def cli_set_token(kubernaut, token) -> None:
    kubernaut.update_config("token", token)
