from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from flask.testing import FlaskClient



@pytest.fixture
def client() -> "FlaskClient":
    from app import flask_app
    import app.views  # noqa

    return flask_app.test_client()
