"""Security functions for the API"""

import re
import requests
import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask


def classify_user_agent(ua: str) -> str:
    """Regex pattern to match common fake user agents"""

    fake_user_agent_pattern = re.compile(
        r"(bot|spider|crawl|slurp|Mediapartners-Google|fake|Windows NT 9\.0|Windows Phone|compatible; MSIE|Trident/["
        r"0-9])",
        re.IGNORECASE,
    )

    # Regex pattern to match known real user agents
    real_user_agent_pattern = re.compile(
        r"(Mozilla|AppleWebKit|Chrome|Safari|Firefox|MSIE|Opera|Trident)", re.IGNORECASE
    )

    # Regex pattern to match suspicious user agents
    suspicious_user_agent_pattern = re.compile(
        r"(^Mozilla\\d+\.\d+ \([\w\s]+\)$|^\w+-\w+-\w+ \([\w\s]+\)$)", re.IGNORECASE
    )

    if fake_user_agent_pattern.search(ua):
        return "fake"
    elif real_user_agent_pattern.search(ua):
        return "real"
    elif suspicious_user_agent_pattern.search(ua):
        return "suspicious"
    else:
        return "unknown"


def get_latest_vpn_list() -> list[str]:
    response = requests.get("https://github.com/X4BNet/lists_vpn/raw/main/output/vpn/ipv4.txt")
    return response.text.splitlines()


def classify_ipv4_for_vpn(app: "Flask", ip: str) -> str:
    """Check if an IPV4 is found in common VPN addresses.

    List is cached and updated every 24 hours.

    Arguments:
        app ("Flask"): the flask object to extract last download time from
        ip (str): ip to check in the list for

    Uses this list: https://github.com/X4BNet/lists_vpn
    """

    time_difference = datetime.datetime.now() - app.last_vpn_download_time  # type: ignore

    if time_difference.total_seconds() >= 86400:  # type: ignore

        # mypy wont let monkey patch
        app.last_vpn_download_time = datetime.datetime.now()  # type: ignore
        app.list_vpns = get_latest_vpn_list()  # type: ignore

    if ip in app.list_vpns:  # type: ignore
        return "likely a vpn"
    else:
        return "likely not a vpn"

