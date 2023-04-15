from typing import Union, Any

from flask import Response


def test_cdn(client: Any, captcha_data: dict):
    """Check normal route usage"""
    response: Union[Response, Any] = client.get(captcha_data["cdn_url"])
    assert isinstance(response, Response)


def test_max_usage(client: Any, captcha_data: dict):
    """Check to see if max usage param. works"""
    client.get(captcha_data["cdn_url"])
    response = client.get(captcha_data["cdn_url"])

    assert response.status_code == 418


def test_bad_url(client: Any, captcha_data: dict):
    """Check with a bad URL"""
    response = client.get(captcha_data["cdn_url"] + "ThisWillNotExist")

    assert response.status_code == 400
