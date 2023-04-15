from typing import Union, Any

from flask import Response


def test_solution(client: Any, captcha_data: dict):
    """Check normal route usage"""
    response: Union[Response, Any] = client.post(
        captcha_data["solution_check_url"],
        json={
            "attempt": client.application.captchas_solution[
                captcha_data["solution_id"]
            ]["solution"]
        },
    )

    assert response.json == {
        "case_sensitive_correct": True,
        "case_insensitive_correct": True,
    }


def test_max_checked(client: Any, captcha_data: dict):
    """Check max allowed check attempts"""
    client.post(captcha_data["solution_check_url"])
    response: Union[Response, Any] = client.post(captcha_data["solution_check_url"])

    assert response.status_code == 418


def test_bad_id(client: Any, captcha_data: dict):
    """Check normal route usage"""
    response: dict = client.post(
        captcha_data["solution_check_url"] + "ThisDoesNotExist"
    ).json

    assert response["text"] == "solution_id not found"
