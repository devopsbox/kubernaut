from kubernaut.schema import load_schema

import jsonschema


def validate_claim_config(config):
    jsonschema.validate(config, load_schema("claim_config.json"))
