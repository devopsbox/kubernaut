import datetime


class KubernautServiceException(Exception):

    def __init__(self, **kwargs):
        super(KubernautServiceException, self).__init__(format_message(**kwargs))
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


def format_message(**kwargs):
    return """An error has occurred!
        
{0}
        
Status: {1} - {2}
ID:     {3}
""".format(kwargs["message"], kwargs["http_status"], kwargs["code"], kwargs["error_id"]).strip()
