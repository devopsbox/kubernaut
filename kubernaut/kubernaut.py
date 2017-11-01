import collections
import errno
import json
import os

from kubernaut import DEFAULT_CLAIM_NAME

from .exception import *
from .kubernaut_http import KubernautHttpClient
from pathlib2 import Path

kubeconfig_root = Path.home() / ".kube"

config_root = Path.home() / ".config" / "kubernaut"
config_file = config_root / "config.json"

Claim = collections.namedtuple("Claim", ["name", "kubeconfig"])


class Kubernaut(object):

    def __init__(self, host, **kwargs):
        self.host = host
        self.config = kwargs

    def claim(self, **kwargs):
        http = self.http_client()
        (status, headers, content) = http.claim(**kwargs)

        if status == 200:
            claim = Claim(**content)

            kubeconfig_root.mkdir(exist_ok=True)
            kubeconfig_name = get_kubeconfig_name(claim.name)
            with (kubeconfig_root / kubeconfig_name).open("w+") as f:
                f.write(claim.kubeconfig)

            return claim, kubeconfig_root / kubeconfig_name
        else:
            raise create_kubernaut_service_exception(status, content)

    def discard(self, name):
        http = self.http_client()
        (status, headers) = http.discard(name)
        if status == 204:
            try:
                os.remove(str(kubeconfig_root / get_kubeconfig_name(name)))
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
        else:
            return False

    def list_claims(self):
        pass

    def get_kubeconfig(self, claim_name):
        http = self.http_client()
        (status, headers, content) = http.get_claim(claim_name)

        if status == 200:
            claim = Claim(**content)

            kubeconfig_root.mkdir(exist_ok=True)
            kubeconfig_name = get_kubeconfig_name(claim.name)
            with (kubeconfig_root / kubeconfig_name).open("w+") as f:
                f.write(claim.kubeconfig)

            return claim, kubeconfig_root / kubeconfig_name
        else:
            raise create_kubernaut_service_exception(status, content)

    def update_config(self, key, value):
        if any(v is None for v in [key]) is None:
            raise ValueError("Config key or host cannot be null")

        config = self.config.get(self.host, {})
        config[key] = value

        self.config[self.host] = config
        self.save_config()

    def get_config_value(self, key, required=False):
        config = self.config.get(self.host, {})
        result = config.get(key, None)

        if required and result is None:
            raise ValueError("required config key is missing: {}".format(key))

        return result

    def save_config(self):
        with config_file.open("w+") as f:
            json.dump(self.config, f, indent=2)

    def http_client(self):
        return KubernautHttpClient(api_token=self.get_config_value("token", required=True))


def new_kubernaut(host="kubernaut.io"):
    config_root.mkdir(parents=True, exist_ok=True)

    with config_file.open("a+") as f:
        f.seek(0)
        config = json.loads(f.read() or "{}")
        return Kubernaut(host, **config)


def get_kubeconfig_name(claim_name):
    result = "kubernaut"
    if claim_name != DEFAULT_CLAIM_NAME:
        result += "-{}".format(claim_name)

    return result
