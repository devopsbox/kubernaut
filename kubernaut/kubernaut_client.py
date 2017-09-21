import json
import requests
import click

from . import __version__
from . import defaults


class KubernautClient(object):

    def __init__(self, **kwargs):
        self.api_token = str(kwargs["api_token"])

        scheme = ("https:" if bool(kwargs.get("use_https", True)) else "http:")
        self.base_url = "{0}//{1}:{2}".format(
            scheme,
            kwargs.get("host", defaults.DEFAULT_REMOTE_API_HOST),
            kwargs.get("port", (443 if scheme == "https:" else 80))
        )

    def claim(self, **kwargs):
        url = "{0}/claims".format(self.base_url)

    def discard(self, *names):
        for name in names:
            url = "{0}/claims/{1}".format(self.base_url, name)
            click.echo(url)

    def claim_info(self, name):
        url = "{0}/claims/{1}".format(self.base_url, name)

    def __handle_response(self, resp):
        pass

    def __create_headers(self):
        return {
            "Authorization": "Bearer {0}".format(self.api_token),
            "User-Agent": "kubernaut/{}".format(__version__)
        }
