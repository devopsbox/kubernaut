import requests

from .exception import *
from . import __version__, DEFAULT_REMOTE_API_HOST


class KubernautHttpClient(object):

    def __init__(self, **kwargs):
        self.api_token = str(kwargs["api_token"])

        scheme = ("https:" if bool(kwargs.get("use_https", True)) else "http:")
        self.base_url = "{0}//{1}:{2}".format(
            scheme,
            kwargs.get("host", DEFAULT_REMOTE_API_HOST),
            kwargs.get("port", (443 if scheme == "https:" else 80))
        )

    def claim(self, **kwargs):
        url = "{0}/claims".format(self.base_url)
        payload = {
            "name": kwargs["name"],
            "pool": "default",  # this will be overridable eventually
        }

        resp = requests.post(
            url=url,
            headers=self.__create_headers(),
            json=payload
        )

        return self.__handle_response(resp)

    def get_claim(self, name):
        url = "{0}/claims/{1}".format(self.base_url, name)

        resp = requests.get(
            url=url,
            headers=self.__create_headers()
        )

        return resp.status_code, resp.headers, resp.text

    def discard(self, name):
        url = "{0}/claims/{1}".format(self.base_url, name)
        resp = requests.delete(
            url=url,
            headers=self.__create_headers(),
        )

        return self.__handle_response(resp)

    def __handle_response(self, resp):
        status = resp.status_code

        if status == 401:
            raise KubernautAuthException()
        if status == 500:
            raise KubernautServiceException()

        return status, resp.headers, resp.text or None

    def __create_headers(self):
        return {
            "Authorization": "Bearer {0}".format(self.api_token),
            "User-Agent": "kubernaut/{0}".format(__version__)
        }
