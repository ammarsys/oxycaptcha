<div align="center">

### This repository is currently being remade & the API is not being hosted yet.

# oxycaptcha

<i>Fast, secure, adaptable captcha API made with Flask.</i>

![image](https://cdn.discordapp.com/attachments/995797406404857977/1104183215377354762/image.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

This is a free-to-use, integrate-yourself Captcha API built with Python. 
It provides a Captcha, and it's solution, which makes it possible to be implemented anywhere with a bit of work (e.g. webapps, Discord Bots).

You can find the projects' homepage (and the API documentations) [here](https://google.com/).

## Usage

Examples on how to integrate the API are [here](https://google.com/). However, the usage really boils down
to making simple HTTP requests,

```python
import requests

# This is boilerplate code! It does not work currently as we haven't released v5.0.0 yet.
response = requests.get('https://oxycaptcha.pythonanywhere.com/api/v5/captcha').json()
print(response)
```

## Contributing

Contributions are always welcome! In the [CONTRIBUTING.md](https://github.com/ammarsys/oxycaptcha/blob/main/CONTRIBUTING.md), you will find instructions & current TODO list.


