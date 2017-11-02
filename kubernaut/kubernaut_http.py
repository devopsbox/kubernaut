import logging
import requests

from .exception import *
from . import __version__


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class KubernautHttpClient(object):

    def __init__(self, **kwargs):
        self.api_token = str(kwargs["api_token"])

        self.base_url = "{0}://{1}".format(
            kwargs["remote_addr"].scheme,
            kwargs["remote_addr"].netloc
        )

    def claim(self, **kwargs):
        url = "{0}/claims".format(self.base_url)
        headers = self.__create_headers()

        payload = {
            "name": kwargs["name"],
            "pool": "default",  # this will be overridable eventually
        }

        logger.debug(""">> POST %s

%s""", url, self.__format_header_map(headers))

        resp = requests.post(
            url=url,
            headers=self.__create_headers(),
            json=payload
        )

        logger.debug("""<< POST %s = %s

%s

%s
""", url, resp.status_code, self.__format_header_map(resp.headers), resp.text)

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
        headers = self.__create_headers()

        logger.debug(""">> DELETE %s

%s""", url, self.__format_header_map(headers))

        resp = requests.delete(
            url=url,
            headers=headers,
        )

        logger.debug("""<< DELETE %s = %s

%s""", url, resp.status_code, self.__format_header_map(resp.headers))

        return self.__handle_response(resp)

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

    def __format_header_map(self, headers):

        res = "{:<20} {:<100}\n\n".format('Key', 'Value')
        for k, v in sorted(headers.items()):
            if k == "Authorization":
                v = "<REDACTED>"

            res += "{:<20} {:<100}\n".format(k, v)

        return res
