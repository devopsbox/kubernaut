import errno
import json
import os

from kubernaut import DEFAULT_CLAIM_NAME

from .exception import *
from .kubernaut_http import KubernautHttpClient
from pathlib2 import Path

kubeconfig_root = Path.home() / ".kube"

config_file = "config.json"


class Kubernaut(object):

    def __init__(self, remote_addr, config_root, **kwargs):
        self.remote_addr = remote_addr
        self.config_root = config_root
        self.config = kwargs

    def config_host(self):
        return self.remote_addr.netloc

    def claim(self, **kwargs):
        http = self.http_client()
        try:
            (status, headers, content) = http.claim(**kwargs)
            payload = json.loads(content)

            if status == 200:
                claim = payload["claim"]

                kubeconfig_root.mkdir(exist_ok=True)
                kubeconfig_name = get_kubeconfig_name(claim.name)
                with (kubeconfig_root / kubeconfig_name).open("w+") as f:
                    f.write(claim.kubeconfig)

                return claim, kubeconfig_root / kubeconfig_name
            else:
                raise create_service_click_exception(http_status=status, **(payload.get("error", {})))

        except RequestException as ex:
            raise create_client_click_exception(ex) from ex

    def discard(self, name):
        http = self.http_client()
        try:
            (status, headers, content) = http.discard(name)
            if status == 204:
                try:
                    os.remove(str(kubeconfig_root / get_kubeconfig_name(name)))
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
        http = self.http_client()
        (status, headers, content) = http.get_claim(claim_name)
        payload = json.loads(content)

        if status == 200:
            claim = payload["claim"]
            kubeconfig = claim["kubernetes"]["kubeconfig"]

            kubeconfig_root.mkdir(exist_ok=True)
            kubeconfig_name = get_kubeconfig_name(claim.name)
            with (kubeconfig_root / kubeconfig_name).open("w+") as f:
                f.write(kubeconfig)

            return claim, kubeconfig_root / kubeconfig_name
        else:
            raise create_service_click_exception(http_status=status, **(payload.get("error", {})))

    def update_config(self, key, value):
        if any(v is None for v in [key]) is None:
            raise ValueError("Config key or host cannot be null")

        config = self.config.get(self.config_host(), {})
        config[key] = value

        self.config[self.config_host()] = config
        self.save_config()

    def get_config_value(self, key, required=False):
        config = self.config.get(self.config_host(), {})
        result = config.get(key, None)

        if required and result is None:
            raise KubernautClientException("Required config entry is missing: '{}' (backend: {})".format(
                key,
                self.config_host()
            ))

        return result

    def save_config(self):
        with (self.config_root / config_file).open("w+") as f:
            json.dump(self.config, f, indent=2)

    def http_client(self):
        return KubernautHttpClient(
            remote_addr=self.remote_addr,
            api_token=self.get_config_value("token", required=True)
        )


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
