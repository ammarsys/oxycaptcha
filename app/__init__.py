from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
from flask_cors import CORS

from .utils import TTLCache


class FlaskWithCount(Flask):
    def __init__(self, import_name: str, captcha_count: int = 0, **kwargs) -> None:
        """
        Modified `flask.Flask` with a captcha_count argument to have a universal instance variable for counting them
        """
        super().__init__(import_name, **kwargs)
        self.captcha_count = captcha_count

        CORS(self)


flask_app = FlaskWithCount(__name__)

captcha_cdn: TTLCache[str, dict[str]] = TTLCache(ttl=30)
captchas_solution: TTLCache[str, str] = TTLCache(ttl=30)

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(flask_app)


__all__ = ["flask_app", "captcha_cdn", "captchas_solution", "limiter"]
