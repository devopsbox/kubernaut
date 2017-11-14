import click
import datetime
import traceback

from requests.exceptions import *
from urllib.parse import urlparse
from click.exceptions import *
from uuid import uuid4


client_msg_template = """{0}

Stacktrace => {1}
ID         => {2}  
"""

service_msg_template = """{0}

Status     => {1} -- {2}
ID         => {3}
"""


class KubernautServiceException(ClickException):

    exit_code = 1

    def __init__(self, message):
        ClickException.__init__(self, message)


class KubernautClientException(ClickException):

    exit_code = 2

    def __init__(self, message):
        ClickException.__init__(self, message)


def create_client_click_exception(ex: Exception) -> KubernautClientException:

    """Generates a ClickException for a client side issue (e.g. connection refused, timeout etc.)"""

    stacktrace = traceback.format_exc()
    error_id = str(uuid4())
    error_file = click.format_filename("/tmp/kubernaut-{0}.stacktrace".format(error_id))

    with open(error_file, "w") as f:
        f.write(stacktrace)

    err_desc = "An unknown or unexpected client error occurred. This is a bug and should be reported!"

    if isinstance(ex, ConnectionError):
        remote_addr = urlparse(ex.request.url)
        err_desc = "Remote connection to {} refused. Are you connected to the internet?".format(remote_addr.netloc)
    elif isinstance(ex, Timeout):
        remote_addr = urlparse(ex.request.url)
        err_desc = "Remote connection to {} timed out. Retry in a few moments.".format(remote_addr.netloc)

    return KubernautClientException(
        client_msg_template.format(
            err_desc,
            error_file,
            error_id
        ))


def create_service_click_exception(**kwargs) -> KubernautServiceException:
    err_desc = kwargs.get(
        "description",
        "An unknown or unexpected service error occurred. This is a bug and should be reported!"
    )

    # generate a timestamp for the worst case situation where there is not an ID (really bad bug) so we can correlate
    # against that instead.
    err_id = kwargs.get("id", datetime.datetime.utcnow().isoformat())

    return KubernautServiceException(
        service_msg_template.format(
            err_desc,
            kwargs["http_status"],
            kwargs.get("code", "Service.Error"),
            err_id
        )
    )
