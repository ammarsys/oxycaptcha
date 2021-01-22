from flask import Flask, send_from_directory, render_template, jsonify, redirect
import base64
from PIL import ImageDraw, Image, ImageFont, ImageFilter
import json, secrets, random

app = Flask(__name__)

def load_json():
    with open('./config.json', 'r') as f:
        data = json.load(f)
    return data

def random_char(y):
    str1 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(secrets.choice(str1) for _ in range(y))

font = [
    ImageFont.truetype("./fonts/arial.ttf", 19),
    ImageFont.truetype("./fonts/gadugib.ttf", 19),
    ImageFont.truetype("./fonts/Chalkduster_400.ttf", 19)
]

curr_json = load_json()

@app.route('/get_img/<path>')
def get_img(path):
    try:
        path = path[::-1]
        v1 = base64.b64decode(path.encode('utf-8'))
        return send_from_directory('C:/Users/scorz/Desktop/flaskapi/images/', v1.decode())
    except Exception as e:
        print(e)
        return render_template('404pg.html')

@app.route('/docs')
def docs():
    return redirect('https://docs.google.com/document/d/1sSMj9TFUGgGhSCYjEcHGKib5wSbTCCkw9YaHbGMXkYU/edit?usp=sharing')

@app.route('/api/img')
def api_captcha():
    for _ in range(0, curr_json["number_to_generate"]):
        text_color = (random.randint(150, 255), 255, random.randint(150, 255))
        image_color = (secrets.randbelow(255), random.randint(50, 125), secrets.randbelow(255))

        img = Image.new('RGB', (100, 30), color=image_color)
        d = ImageDraw.Draw(img)

        for _ in range(0, secrets.randbelow(20)):
            d.line((secrets.randbelow(100), secrets.randbelow(100)) + img.size, fill=secrets.randbelow(100))

        text = random_char(5)
        d.text((24, 5), f"{text}", fill=text_color, font=secrets.choice(font))
        imgblur = img.filter(ImageFilter.GaussianBlur(1.1))
        imgblur.save(fr'{curr_json["path"]}/{text}.png')
        captcha2 = f'{text}.png'
        v2 = captcha2.split('.png')[0]
        v3 = base64.b64encode(captcha2.encode('utf-8'))
        dictv1 = {
            "url": f"http://127.0.0.1:5000/get_img/{v3.decode('utf-8')[::-1]}",
            "solution": v2
        }
        return jsonify(dictv1)

@app.route('/')
def home():
    return render_template("index.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404pg.html")

if __name__ == '__main__':
    app.run(debug=True)
