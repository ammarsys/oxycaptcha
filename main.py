from io import BytesIO
from flask import Flask, send_file, render_template, jsonify, request
from PIL import ImageDraw, Image, ImageFont, ImageFilter
from cryptography.encrypt import encrypt
from cryptography.decrypt import decrypt
import secrets
import random


app = Flask(__name__)
CORS(app)


def random_char(y):
    str1 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(secrets.choice(str1) for _ in range(y))


def genMath():
    numbers = range(50, 100)
    numbers2 = range(0, 50)
    operators = ['+', '-']
    return f'{secrets.choice(numbers)}{secrets.choice(operators)}{secrets.choice(numbers2)}'


fonts_lower = [
    ImageFont.truetype("./fonts/lower/gadugib.ttf", 20),
    ImageFont.truetype("./fonts/lower/Chalkduster_400.ttf", 20),
    ImageFont.truetype('./fonts/lower/ShadowsIntoLight-Regular.ttf', 20)
]
fonts_upper = [
    ImageFont.truetype('./fonts/upper/arial.ttf', 35),
    ImageFont.truetype('./fonts/upper/FallingSky-JKwK.ttf', 35),
    ImageFont.truetype('./fonts/upper/TrainOne-Regular.ttf', 35)
]


def gen1(text):
    try:
        text = text.replace('-', '—')
    except KeyError:
        pass
    text_color = 255, 255, 255
    image_color = (secrets.randbelow(200), secrets.choice(range(50, 126)), secrets.randbelow(200))
    img = Image.new('RGB', (280, 70), color=image_color)
    img.load()
    d = ImageDraw.Draw(img)

    for _ in range(1, secrets.choice(range(7, 13))):
        d.line((secrets.randbelow(100), secrets.choice(range(10, 51))) + img.size, fill=(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )

    right, height = 0, 0
    corresponding_font = {}
    for let in text:
        if let.isupper():
            corresponding_font[let] = secrets.choice(fonts_upper)
        elif let.islower():
            corresponding_font[let] = secrets.choice(fonts_lower)
        else:
            corresponding_font[let] = secrets.choice(fonts_lower)

    for count, letter in enumerate(text):
        cords = secrets.choice(range(20, 29)) + right, secrets.choice(range(2, 9)) + height
        d.text(cords, f"{letter}", fill=text_color, font=corresponding_font[letter])
        right += secrets.choice(range(36, 51)) + count
        height += secrets.choice(range(-5, 11))

    imgblur = img.filter(ImageFilter.BoxBlur(secrets.choice([1, 1.2, 1.2])))
    return imgblur


def gen2(text):
    try:
        text = text.replace('-', '—')
    except KeyError:
        pass
    text_color = 255, 255, 255
    image_color = (secrets.randbelow(200), secrets.choice(range(50, 126)), secrets.randbelow(200))

    img = Image.new('RGB', (120, 30), color=image_color)
    d = ImageDraw.Draw(img)
    for _ in range(1, secrets.choice(range(7, 13))):
        d.line((secrets.randbelow(100), secrets.choice(range(10, 51))) + img.size, fill=(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )

    d.text((24, 5), f"{text}", fill=text_color, font=secrets.choice(fonts_lower))
    imgblur = img.filter(ImageFilter.GaussianBlur(1.1))

    return imgblur


@app.route('/api/cdn/<key>')
def get_img(key):
    key = decrypt(key)
    values = key.split('_')

    PILimage = None
    if values[1] == '2':
        PILimage = gen1(text=values[0])
    if values[1] == '1':
        PILimage = gen2(text=values[0])

    output = BytesIO()
    PILimage.convert('RGBA').save(output, format='PNG')
    output.seek(0, 0)

    return send_file(output, mimetype='image/png', as_attachment=False)


@app.route('/api/img')
def api_captcha():
    level = request.args.get('level', default=2, type=int)
    style = request.args.get('style', default='text', type=str)
    txt = random_char(secrets.choice(range(4, 7)))

    if level not in [1, 2]:
        return render_template('invalid_usage.html')

    if style == 'text':
        return jsonify({'solution': txt, 'url': f'http://127.0.0.1:5000/api/cdn/{encrypt(txt + f"_{str(level)}")}'})
    if style == 'math':
        equation = genMath()
        return jsonify({'solution': eval(equation), 'url': f'http://127.0.0.1:5000/api/cdn/{encrypt(equation + f"_{str(level)}")}'})

    return render_template('invalid_usage.html')


@app.route('/docs')
def docs():
    return render_template('docs.html')


@app.route('/')
def home():
    return render_template("index.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404pg.html")


if __name__ == '__main__':
    app.run(debug=True)
