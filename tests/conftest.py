import json
from typing import TYPE_CHECKING, Union, Any

import pytest

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from flask import Response


@pytest.fixture
def client() -> "FlaskClient":
    from app import flask_app
    import app.views  # noqa

    return flask_app.test_client()


@pytest.fixture
def captcha_data(client: "FlaskClient") -> dict:
    response: Union["Response", Any] = client.post(
        "/api/v5/captcha", json={"maxCdnAccess": 1, "maxSolutionCheck": 1}
    )

    print(response)

    return json.loads(response.data)
