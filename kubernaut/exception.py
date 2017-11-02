import datetime

from click.exceptions import *


class KubernautServiceException(ClickException):

    def __init__(self, **kwargs):
        super().__init__(format_message(**kwargs))
        self.http_status = int(kwargs["http_status"])
        self.code = str(kwargs["code"])
        self.error_id = str(kwargs["error_id"])


def create_kubernaut_service_exception(http_status, payload):
    return KubernautServiceException(
        http_status=http_status,
        code=payload["error"]["code"],
        message=payload["error"]["description"],
        error_id=payload["error"].get("id", datetime.datetime.utcnow().isoformat())
    )


def create_click_exception(http_status, payload):
    return ClickException(format_message(http_status=http_status, **payload["error"]))


def format_message(**kwargs):
    return """{0}
        
Status: {1} - {2}
ID:     {3}
""".format(kwargs["description"], kwargs["http_status"], kwargs["code"], kwargs["id"]).strip()
