from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

# Default name to associate with a claim
DEFAULT_CLAIM_NAME = "main"

# Default name to search for a kubernaut config file in a project directory
DEFAULT_CLAIM_FILE = "kubernaut.yaml"

# Default remote Kubernaut host
DEFAULT_REMOTE_API_ADDR = "https://kubernaut.io:443"
