import os
import tempfile

os.environ["SCOUT_DISABLE"] = "1"
os.environ["HOME"] = str(tempfile.TemporaryDirectory(prefix="kubernaut-"))

os.environ["KUBERNAUT_HOST"] = "localhost:5000"


def get_config(config_root="{}/.config/kubernaut".format(os.environ["HOME"])):
    import json

    with open("{}/config.json".format(config_root)) as f:
        return json.load(f)
