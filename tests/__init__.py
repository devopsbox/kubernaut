import json
import pkg_resources


def load_output(name):
    return pkg_resources.resource_string(__name__, "/".join(("outputs", name))).decode("utf-8")


def get_config(pytest_tempdir):
    config_file = pytest_tempdir.join(".config", "kubernaut", "config.json")
    return json.load(config_file)


def set_token(pytest_tempdir, host, token):
    config_file = pytest_tempdir.mkdir(".config").mkdir("kubernaut").join("config.json")

    with open(str(config_file), 'w') as f:
        data = {host: {"token": token}}
        json.dump(data, f)
