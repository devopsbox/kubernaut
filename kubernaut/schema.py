import json
import pkg_resources


def load_schema(name):
    schema = pkg_resources.resource_string(__name__, "/".join(("jsonschema", name)))
    return json.loads(schema.decode("UTF-8"))
