"""A lightweight Captcha API"""

if __name__ == "__main__":
    from app import flask_app
    from app.views import *

    flask_app.run()
