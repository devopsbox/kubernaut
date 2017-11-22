import logging
import requests

from .logging import *
from .exception import *
from . import __version__


logging.basicConfig()
logger = logging.getLogger("kubernaut.http")
logger.setLevel(logging.INFO)


class KubernautHttpClient(object):

    def __init__(self, **kwargs):
        self.api_token = str(kwargs["api_token"])

        self.base_url = "{0}://{1}".format(
            kwargs["remote_addr"].scheme,
            kwargs["remote_addr"].netloc
        )

    def claim(self, **kwargs):
        method = "POST"
        url = "{0}/claims".format(self.base_url)
        headers = self.__create_headers()

        payload = {
            "name": kwargs["name"],
            "pool": "default",  # this will be overridable eventually
        }

        resp = self.__send_request(method, url, headers, json=payload)
        return self.__handle_response(resp)

    def get_claim(self, name):
        method = "GET"
        url = "{0}/claims/{1}".format(self.base_url, name)
        headers = self.__create_headers()

        resp = self.__send_request(method, url, headers)
        return self.__handle_response(resp)

    def discard(self, name):
        method = "DELETE"
        url = "{0}/claims/{1}".format(self.base_url, name)
        headers = self.__create_headers()

        resp = self.__send_request(method, url, headers)
        return self.__handle_response(resp)

    def __send_request(self, method, url, headers, json=None):
        timeout = 10.000 # make this configurable somehow
        method = method.upper()
        log_http_request(method, url, headers)

        if method == "GET":
            resp = requests.get(url=url, headers=headers, timeout=timeout)
        elif method == "POST":
            resp = requests.post(url=url, headers=headers, timeout=timeout, json=json)
        elif method == "PUT":
            resp = requests.put(url=url, headers=headers, timeout=timeout, json=json)
        elif method == "DELETE":
            resp = requests.delete(url=url, headers=headers, timeout=timeout, json=json)
        else:
            # would prefer to just use this code... but it's a PITA to mock with requests-mock
            resp = requests.request(method=method, url=url, headers=headers, timeout=timeout, json=json)

        log_http_response(resp)
        return resp

    def __handle_response(self, resp):
        status = resp.status_code

        if status == 401:
            raise KubernautServiceException("Authentication for {} failed.".format(self.base_url))

        return status, resp.headers, resp.text or None

    def __create_headers(self):
        return {
            "Authorization": "Bearer {0}".format(self.api_token),
            "User-Agent": "kubernaut/{0}".format(__version__)
        }
