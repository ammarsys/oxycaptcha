"""A lightweight Captcha API"""

import secrets
import datetime
import base64
from io import BytesIO
from urllib.parse import urljoin

from flask import Flask, send_file, render_template, jsonify, redirect, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils import cap_gen, TTLCache

app = Flask(__name__)
app.captcha_count = 0  # type: ignore

CORS(app)
captcha_cdn: TTLCache[str, list] = TTLCache(ttl=30)
captchas_solution: TTLCache[str, str] = TTLCache(ttl=30)

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)


def id_generator(y: int) -> str:
    """
    Generates a captcha ID string of length 'y'.

    Args:
        y (int): The length of the captcha ID string to be generated.

    Returns:
        str: The captcha ID string of length 'y' generated by calling the 'choice' function on the given sequence of
            characters.

    """
    string = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKMNOPQRSTUVWXYZ"
    return "".join(secrets.choice(string) for _ in range(y))


@app.route("/api/v5/cdn/<key>", methods=["GET"])
@limiter.limit("30/minute")
def get_img(key: str):
    """
    A Content Delivery Network (CDN) for serving captcha images.

    Args:
        key (str): The captcha identifier for which the image needs to be served.

    Returns:
        PIL.Image.Image: The captcha image corresponding to the given identifier.

    """
    try:
        if captcha_cdn[key][3] >= captcha_cdn[key][4]:
            del captcha_cdn[key]

        captcha_cdn[key][3] += 1

        if not captcha_cdn[key][1]:
            pil_image = cap_gen(text=captcha_cdn[key][0])
            captcha_cdn[key][1] = pil_image
        else:
            pil_image = captcha_cdn[key][1]

        output = BytesIO()
        pil_image.convert("RGBA").save(output, format="PNG")
        output.seek(0, 0)

        return send_file(output, mimetype="image/png", as_attachment=False)

    except KeyError:
        return redirect("/")


@app.route("/api/v5/captcha", methods=["GET"])
@limiter.limit("30/minute")
def api_captcha():
    """
    Endpoint for creating a dictionary key with the captcha ID and its related information. This route has an argument
    which indicates times the captcha image can be accessed before it is wiped from the dictionary.

    Returns:
        dict: A JSON dictionary containing the captcha ID and its related information.

    """
    access = request.args.get("requests", default=10, type=int)

    if access > 20:
        return redirect("/")

    delta = datetime.timedelta(minutes=5)
    now = datetime.datetime.utcnow()
    time_now = now.strftime("%S")[-5:]

    solution_id = base64.b64encode(
        bytes(
            f"{app.captcha_count}.{id_generator(y=10)}.{time_now}",
            "utf-8",
        )
    ).decode()
    solution = id_generator(y=secrets.choice((4, 5)))
    captchas_solution[solution_id] = solution

    cdn_id = base64.b64encode(
        bytes(
            f"{app.captcha_count}.{id_generator(y=10)}.{time_now}",
            "utf-8",
        )
    ).decode()
    captcha_cdn[cdn_id] = [solution, None, now + delta, 0, access]

    app.captcha_count += 1

    return jsonify(
        {
            "cdn_url": urljoin(request.host_url, f"/api/v5/cdn/{cdn_id}"),
            "solution_check_url": urljoin(
                request.host_url, f"/api/v5/check/{solution_id}"
            ),
            "solution_id": solution_id,
            "cdn_id": cdn_id,
        }
    )


@app.route("/api/v5/check/<solution_id>", methods=["POST"])
@limiter.limit("10/minute")
def check_solution(solution_id: str):
    data = {"correct": False, "case_insensitive_correct": False}

    attempt = request.args.get("solution", type=str, default="x")
    solution = captchas_solution.get(solution_id)

    if attempt == solution:  # type: ignore
        data["correct"] = True

    if attempt.lower() == solution.lower():  # type: ignore
        data["case_insensitive_correct"] = True

    return jsonify(data)


@app.route("/examples", methods=["GET"])
def examples():
    """API examples endpoint"""
    return render_template("examples.html")


@app.route("/", methods=["GET"])
def home():
    """API home"""
    return render_template("index.html")


@app.errorhandler(404)
def not_found(_):
    """404 error handling"""
    return redirect("/")


if __name__ == "__main__":
    app.run()
