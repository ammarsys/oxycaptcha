from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
from flask_cors import CORS

from .utils import TTLCache

flask_app = Flask(__name__)
flask_app.captcha_count = 0
CORS(flask_app)

captcha_cdn: TTLCache[str, list] = TTLCache(ttl=30)
captchas_solution: TTLCache[str, str] = TTLCache(ttl=30)

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(flask_app)


__all__ = ["flask_app", "captcha_cdn", "captchas_solution", "limiter"]
