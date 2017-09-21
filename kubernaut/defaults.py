from pathlib2 import Path

# Default location where the config file lives
DEFAULT_CONFIG_FILE = Path.home() / ".config" / "kubernaut" / "config.json"

# Default name to associate with a claim
DEFAULT_CLAIM_NAME = "default"

# Default name to search for a kubernaut config file in a project directory
DEFAULT_CLAIM_FILE = "kubernaut.yaml"

DEFAULT_REMOTE_API_HOST = "kubernaut.io"
