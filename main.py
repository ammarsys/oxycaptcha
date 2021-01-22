from flask import Flask, send_from_directory, render_template, jsonify, redirect
import os, secrets, base64

app = Flask(__name__)

@app.route('/get_img/<path>')
def get_img(path):
    try:
        path = path[::-1]
        v1 = base64.b64decode(path.encode('utf-8'))
        return send_from_directory('C:/Users/scorz/Desktop/flaskapi/images/', v1.decode())
    except:
        return render_template('404pg.html')

@app.route('/docs')
def docs():
    return redirect('https://docs.google.com/document/d/1sSMj9TFUGgGhSCYjEcHGKib5wSbTCCkw9YaHbGMXkYU/edit?usp=sharing')

@app.route('/api/img')
def api_captcha():
    captcha2 = secrets.choice(os.listdir("./images"))
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
