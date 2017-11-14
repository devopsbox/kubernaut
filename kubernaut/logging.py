import logging

from requests import Response
from typing import Dict


def log_http_response(response: Response):
    logger = logging.getLogger("kubernaut.http")

    logger.debug(""" --- Response ---
Status = {status} {ok} 
URL    = {url}

--- Headers ---
{headers}

--- Content ---
{content}
""".format(status=response.status_code,
           ok=response.ok,
           url=response.url,
           headers=format_http_headers(response.headers),
           content=format_content(response.text, None)))


def log_http_request(method, url, headers, content=None, json=None):
    logger = logging.getLogger("kubernaut.http")

    logger.debug(""" --- Request ---
Method = {method}
URL    = {url}

--- Headers ---
{headers}

--- Content ---
{content}
""".format(method=method,
           url=url,
           headers=format_http_headers(headers),
           content=format_content(content, json)))


def format_http_headers(headers: Dict[str, str]) -> str:
    res = ""

    if len(headers) == 0:
        return "<NO HEADERS>"

    longest_header = len(max(list(headers.keys()), key=len))
    value_truncate = 80 - longest_header
    header_padding = longest_header

    format_str = "{:<" + str(header_padding) + "} = {:." + str(value_truncate) + "}"

    header_count = 0
    for (name, value) in sorted(headers.items()):
        header_count += 1

        if "AUTHORIZATION" in name.upper():
            value = "<REDACTED>"

        if header_count != len(headers):
            res += format_str.format(name, value) + "\n"
        else:
            res += format_str.format(name, value)

    return res


def format_content(data, json) -> str:
    if data is not None:
        return data
    elif json is not None:
        import json as json_serializer
        return json_serializer.dumps(json, indent=2, sort_keys=True)
    else:
        return "<NO CONTENT>"
