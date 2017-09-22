from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

# Default name to associate with a claim
DEFAULT_CLAIM_NAME = "default"

# Default name to search for a kubernaut config file in a project directory
DEFAULT_CLAIM_FILE = "kubernaut.yaml"

# Default remote Kubernaut host
DEFAULT_REMOTE_API_HOST = "kubernaut.io"
