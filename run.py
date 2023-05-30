"""A lightweight Captcha API"""

from app import flask_app  # noqa
from app.views import *

app = flask_app

if __name__ == "__main__":
    app.run()
