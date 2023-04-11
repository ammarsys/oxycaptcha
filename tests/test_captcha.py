from typing import TYPE_CHECKING, Union, Any
import json

if TYPE_CHECKING:
    from flask import Response


def test_api_captcha_internal(client: Any):
    """Check normal route usage"""
    response: Union["Response", Any] = client.post("/api/v5/captcha", json={"maxCdnAccess": 5, "maxSolutionCheck": 5})
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "cdn_url" in data
    assert "solution_check_url" in data
    assert "solution_id" in data
    assert "cdn_id" in data

    # Check internally to see if the captcha is actually there
    assert client.application.captcha_cdn.get(data["cdn_id"], None)
    assert client.application.captchas_solution.get(
        client.application.captcha_cdn[data["cdn_id"]]["solution_id"], None
    )

    # GC
    del client.application.captchas_solution[client.application.captcha_cdn[data["cdn_id"]]["solution_id"]]
    del client.application.captcha_cdn[data["cdn_id"]]



def test_api_captcha_maxcdnaccess(client: Any):
    """Check error handling"""
    response = client.post("/api/v5/captcha", json={"maxCdnAccess": 25, "maxSolutionCheck": 5})
    assert response.status_code == 400

    data = json.loads(response.data)
    assert data["type"] == "error"

    assert "maxCdnAccess is over 20." in data["text"]


def test_api_captcha_maxsolution_check(client: Any):
    """Check error handling"""
    response = client.post("/api/v5/captcha", json={"maxCdnAccess": 5, "maxSolutionCheck": 25})
    assert response.status_code == 400

    data = json.loads(response.data)
    assert data["type"] == "error"

    assert "maxSolutionCheck is over 20." in data["text"]
