# This repository is currently being remade

The new version comes with a lot of features and a prettier front end. Chip in by leaving a ⭐ & wait for the v2 version.

# Captcha API

A lightweight Captcha API made with Flask. This version is a new, fast and completely rewritten API, originally by Vixen, which was discontinued.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

The API is live at [PythonAnywhere](https://pythonanywhere.com/) (specifically, [here](https://captchaAPI.pythonanywhere.com/)). 
# Usage

### Wrappers

 - [JavaScript](https://www.npmjs.com/package/essentials-captcha)
 - [Repository & Creator](https://github.com/SpeckyYT/essentials-captcha#readme)

### Manual Usage

Simply make a HTTP get request to the API endpoint and treat it like a JSON.

```python
import requests

response = requests.get('https://captchaAPI.pythonanywhere.com/api/img').json()

print(response["solution"], response["url"])
```

or, if you'd like a async request

```python
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://captchaAPI.pythonanywhere.com/api/img') as responseget:
            return await responseget.json()

loop = asyncio.get_event_loop()
response = loop.run_until_complete(main())
print(response["solution"], response["url"])
```

For more examples check out https://captchaAPI.pythonanywhere.com/examples !

*For contributing please check out `CONTRIBUTING.md`*

# Documentations

- ## <span style="color:white">/api/img</span>
`Method:` get

`Return Type:` text / json

`Description:` URL (CDN) of the captcha and it's solution.

### **Parameters**

- requests

`Type:` number

`Default Value | Max Value:` 10 | 20

`Description:` The number of how many times the image can be accessed before it expires.

<hr>

- ## <span style="color:white">/api/cdn/&lt;key&gt;</span>
`Method:` get

`Return Type:` image

`Description:` An image (the captcha).
