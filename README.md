<div align="center">

<h1> <span style="color: #1a68c5;">oxy</span>captcha </h1>

<i>Fast, secure, adaptable captcha API made with Flask.</i>

![image](https://cdn.discordapp.com/attachments/995797406404857977/1104183215377354762/image.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

This is a free-to-use, integrate-yourself Captcha API built with Python. 
It provides a Captcha, and it's solution, which makes it possible to be implemented anywhere with a bit of work (e.g. webapps, Discord Bots).

You can find the projects' homepage [here](https://oxycaptcha.pythonanywhere.com/).

## Usage

The usage really boils down to making simple HTTP requests,

```python
import requests
from io import BytesIO
from PIL import Image

captcha_data = requests.post("https://oxycaptcha.pythonanywhere.com/api/v5/captcha").json()
captcha_image_content = requests.get(captcha_data["cdn_url"]).content

# Show the image to the user
Image.open(BytesIO(captcha_image_content)).show()
attempt = input("What does the captcha say? >> ")

solution_check = requests.post(
    captcha_data["solution_check_url"], 
    json={"attempt": attempt}
).json()

if solution_check["case_sensitive_correct"] == True:
    print("Good job! That attempt was right.")
else:
    print("Err, not quite.")
```

## API Documentations

You can find the API documentations [here](https://oxycaptcha.pythonanywhere.com/docs).

## Contributing

Contributions are always welcome! In the [CONTRIBUTING.md](https://github.com/ammarsys/oxycaptcha/blob/main/CONTRIBUTING.md), you will find instructions & current TODO list.


