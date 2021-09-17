"""
A lightweight Captcha API made with Flask. This version is a new, fast and completely rewritten API,
originally by Vixen, which was discontinued.

The website is located at https://ammarsysdev.pythonanywhere.com/

License: MIT
"""

# Standard library imports
import secrets
import datetime
import base64
from typing import Callable
from io import BytesIO

# Related third party imports
from flask import (
    Flask,
    send_file,
    render_template,
    jsonify,
    redirect,
    request
)
from flask_cors import CORS
from PIL import ImageDraw, Image, ImageFont
import random
import expiringdict

# Local application/library specific imports
from utils import noise

app = Flask(__name__)
CORS(app)
captchas = expiringdict.ExpiringDict(max_age_seconds=120, max_len=float('inf'))


class CaptchaCount:
    """Class to count captchas to prevent duplicates in the captchas dictionary."""
    count: int = 0


fonts_lower = [
    ImageFont.truetype("./fonts/lower/gadugib.ttf", 32),
    ImageFont.truetype("./fonts/lower/Chalkduster_400.ttf", 32),
    ImageFont.truetype('./fonts/lower/ShadowsIntoLight-Regular.ttf', 32),
    ImageFont.truetype('./fonts/lower/Rajdhani-SemiBold.ttf', 32)
]
fonts_upper = [
    ImageFont.truetype('./fonts/upper/arial.ttf', 55),
    ImageFont.truetype('./fonts/upper/FallingSky-JKwK.ttf', 55),
    ImageFont.truetype('./fonts/upper/TrainOne-Regular.ttf', 55),
    ImageFont.truetype('./fonts/upper/BebasNeue-Regular.ttf', 55)
]


def id_generator(y: int, choice: Callable) -> str:
    """
    Generate captcha Is. Accepts either secrets or random, depending on if the use case needs to be cryptographically
    secure.

    :param y: string length
    :type y: int
    :param choice: module to use
    :type choice: Callable
    :return: string in form of an ID
    """
    string = 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKMNOPQRSTUVWXYZ'
    return ''.join(choice(string) for _ in range(y))


def cap_gen(text: str) -> Image.Image:
    """
    Generate captchas for the API.

    :param text: the captcha text
    :type text: str
    :return: an image in form of Image.Image
    """
    white = 255, 255, 255
    space, height = random.randint(5, 10), random.randint(5, 10)

    corresponding_font = {
        let: random.choice(
            fonts_upper if let.isupper() else fonts_lower
        )
        for let in text
    }
    text_positions = []

    img = Image.new('RGB', (300, 100), color=(128, 128, 128))
    img.load()

    d = noise.add_noise_lines(ImageDraw.Draw(img))

    for count, letter in enumerate(text):
        cords = space, height
        d.text(cords, f"{letter}", fill=white, font=corresponding_font[letter])

        space += secrets.choice(range(35, 45))
        height += secrets.choice(range(1, 11))

        text_positions.append(
            tuple(secrets.randbelow(10) + 15 + i for i in cords)
        )

    value = secrets.randbelow(len(text_positions))
    for i in range(len(text_positions) - value):
        d.line((text_positions[i], text_positions[i + value]), fill=white, width=0)

    return img


@app.route('/api/cdn/<key>')
def get_img(key: str):
    """
    CDN (Content Delivery Network) for the captchas.

    :param key: the captcha identifier
    :type key: str
    """
    try:
        if captchas[key][3] >= captchas[key][4]:
            del captchas[key]

        captchas[key][3] += 1

        if not captchas[key][1]:
            pil_image = noise.salt_and_pepper(cap_gen(text=captchas[key][0]), prob=0.13)
            captchas[key][1] = pil_image
        else:
            pil_image = captchas[key][1]

        output = BytesIO()
        pil_image.convert('RGBA').save(output, format='PNG')
        output.seek(0, 0)

        return send_file(output, mimetype='image/png', as_attachment=False)

    except KeyError:
        return redirect('/')


@app.route('/api/img')
def api_captcha():
    """
    The endpoint for creating dictionary key with the captcha ID, it's values being the information about image,
    meaning that images are not generated here. Takes a access paramater that represents the number of how many times
    the image can be accessed before it's wiped from the dictionary.

    :return: JSON dictionary
    """
    access = request.args.get('requests', default=10, type=int)

    if access > 20:
        return redirect('/')

    delta = datetime.timedelta(minutes=5)
    now = datetime.datetime.utcnow()

    solution = id_generator(y=secrets.choice((4, 6)), choice=secrets.choice)

    id_ = base64.b64encode(
        bytes(
            f'{CaptchaCount.count}.{id_generator(y=10, choice=random.choice)}.{now.strftime("%S")[-5:]}', 'utf-8'
        )
    ).decode()

    captchas[id_] = [solution, None, now + delta, 0, access]
    CaptchaCount.count += 1

    return jsonify({
        'solution': solution,
        'url': f'http://127.0.0.1:5000/api/cdn/{id_}'
    })


@app.route('/examples')
def examples():
    """API examples endpoint"""
    return render_template("examples.html")


@app.route('/')
def home():
    """API home"""
    return render_template("index.html")


@app.errorhandler(404)
def not_found(e):
    """404 error handling"""
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
