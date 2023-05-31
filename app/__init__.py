from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
from flask_cors import CORS

from .utils import TTLCache


class FlaskAdapted(Flask):
    def __init__(self, import_name: str, captcha_count: int = 0, **kwargs) -> None:
        """
        Modified `flask.Flask` to include captcha_count and TTL cache captcha storage implementations
        """
        super().__init__(import_name, **kwargs)
        self.captcha_count = captcha_count

        self.captcha_cdn: TTLCache[str, dict] = TTLCache(ttl=60)
        self.captchas_solution: TTLCache[str, dict] = TTLCache(ttl=90)

        CORS(self)


flask_app = FlaskAdapted(__name__)

limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")
limiter.init_app(flask_app)


__all__ = ["flask_app", "limiter"]
