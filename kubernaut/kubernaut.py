import errno
import json
import os

from kubernaut import DEFAULT_CLAIM_NAME

from .exception import *
from .kubernaut_http import KubernautHttpClient
from pathlib2 import Path

config_file = "config.json"


class Kubernaut(object):

    def __init__(self, remote_addr, config_root, **kwargs):
        self.kubeconfig_root = Path.home() / ".kube"
        self.remote_addr = remote_addr
        self.config_root = config_root
        self.config = kwargs

    def config_host(self):
        return self.remote_addr.netloc

    def claim(self, **kwargs):
        http = self.new_http_client()
        try:
            (status, headers, content) = http.claim(**kwargs)
            payload = self.__get_payload(status, headers, content)

            if status == 200:
                claim = payload["claim"]

                self.kubeconfig_root.mkdir(exist_ok=True)
                kubeconfig_name = get_kubeconfig_name(claim["name"])
                with (self.kubeconfig_root / kubeconfig_name).open("w+") as f:
                    f.write(claim["kubernetes"]["kubeconfig"])

                return claim, self.kubeconfig_root / kubeconfig_name
            else:
                raise create_service_click_exception(http_status=status, **(payload.get("error", {})))

        except RequestException as ex:
            raise create_client_click_exception(ex) from ex

    def discard(self, name):
        http = self.new_http_client()
        try:
            (status, headers, content) = http.discard(name)
            if status == 204:
                try:
                    os.remove(str(self.kubeconfig_root / get_kubeconfig_name(name)))
                except OSError as e:
                    if e.errno != errno.ENOENT:
                        raise
            else:
                return False
        except RequestException as ex:
            raise create_client_click_exception(ex) from ex

    def list_claims(self):
        pass

    def get_kubeconfig(self, claim_name):
        http = self.new_http_client()
        try:
            (status, headers, content) = http.get_claim(claim_name)
            payload = self.__get_payload(status, headers, content)

            if status == 200:
                claim = payload["name"]
                kubeconfig = claim["kubernetes"]["kubeconfig"]

                self.kubeconfig_root.mkdir(exist_ok=True)
                kubeconfig_name = get_kubeconfig_name(claim.name)
                with (self.kubeconfig_root / kubeconfig_name).open("w+") as f:
                    f.write(kubeconfig)

                return claim, self.kubeconfig_root / kubeconfig_name
            else:
                raise create_service_click_exception(http_status=status, **(payload.get("error", {})))
        except RequestException as ex:
            raise create_client_click_exception(ex) from ex

    def update_config(self, key, value):
        if any(v is None for v in [key]) is None:
            raise ValueError("Config key or host cannot be null")

        config = self.config.get(self.config_host(), {})
        config[key] = value

        self.config[self.config_host()] = config
        self.save_config()

    def get_config_value(self,
                         key,
                         required=False,
                         required_msg="Required config entry is missing: '{}' (backend: {})"):

        config = self.config.get(self.config_host(), {})
        result = config.get(key, None)

        if required and result is None:
            raise KubernautClientException(required_msg.format(
                key,
                self.config_host()
            ))

        return result

    def save_config(self):
        with (self.config_root / config_file).open("w+") as f:
            json.dump(self.config, f, indent=2)

    def new_http_client(self):
        from kubernaut.messages import GET_TOKEN

        return KubernautHttpClient(
            remote_addr=self.remote_addr,
            api_token=self.get_config_value("token", required=True, required_msg=GET_TOKEN)
        )

    def __get_payload(self, status, headers, content):
        content_type = headers['content-type']
        if not content_type.startswith("application/json"):
            raise create_service_click_exception(
                http_status=status,
                description="Unexpected or incorrect content type received from service "
                            "(expected: {}, received: {})".format("application/json", content_type),
            )

        return json.loads(content)


def new_kubernaut(host, config_root):
    config_root.mkdir(parents=True, exist_ok=True)

    with (config_root / config_file).open("a+") as f:
        f.seek(0)
        config = json.loads(f.read() or "{}")
        return Kubernaut(host, config_root, **config)


def get_kubeconfig_name(claim_name):
    result = "kubernaut"
    if claim_name != DEFAULT_CLAIM_NAME:
        result += "-{}".format(claim_name)

    return result
