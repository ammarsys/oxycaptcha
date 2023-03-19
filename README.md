<hr>

## This repository is currently being remade & the API is not being hosted yet.
<hr>

<div align="center">

# Captcha API

<i>Fast, secure, adaptable Captcha API made in Flask.</i>

![image](https://cdn.discordapp.com/attachments/1085992233536335982/1086430183604629564/image.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

This is a free-to-use, integrate-yourself Captcha API built with Python. 
It provides a Captcha, and it's solution, which makes it possible to be implemented anywhere with a bit of work (e.g. webapps, Discord Bots).

You can find the projects' homepage (and the API documentations) [here](https://google.com/).

## Usage

You can find examples on how to integrate the API [here](https://google.com/). However, the usage really boils down
to making simple HTTP requests,

```python
import requests

response = requests.get('https://captchaAPI.pythonanywhere.com/api/img').json()

print(response["solution"], response["url"])
```

## Contributing

Contributions are always welcome! In the [CONTRIBUTING.md](https://github.com/ammarsys/captchaAPI/blob/main/CONTRIBUTING.md), you will find instructions & current TODO list.


