from typing import Any


def test_proper_insertion(client: Any, captcha_data: dict):
    """Check normal usage"""
    _ = client.get(captcha_data["cdn_url"])

    assert len(client.application.captcha_cdn)
