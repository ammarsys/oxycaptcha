# Captcha API
### *By Ammar*
![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)

[![CC-0 license](https://img.shields.io/badge/License-CC--0-blue.svg)](https://creativecommons.org/licenses/by-nd/4.0)

## Info
I made this API so I can use it alongside [Essentials Discord Bot](https://github.com/Ammar-sys/essentials) and I've decided to make it public. The API is live at [PythonAnywhere](https://ammarsysdev.pythonanywhere.com/). Tell me [here](https://github.com/Ammar-sys/captchaAPI/issues) if you run into issues

## USAGE

### Wrappers

 - [JavaScript](https://www.npmjs.com/package/essentials-captcha)
 - [Repository & Creator](https://github.com/SpeckyYT/essentials-captcha#readme)

### Manual Install
 
 Make sure to go through the files and edit paths. (both py files)
 
 To install the necessary modules for this to run do

```python
pip install requirements.txt
``` 

Incase that doesn't work, try:

```python
py -m pip install requirements.txt
```

It's recommended to run both clean_up.py and main.py. Clean_up.py deletes captchas in the folder in order to save storage

Its intended for discord bots BUT it can be used for web development (if you don't really care about good security) and other projects as the image has basic encryption. You may want to make it a bit more tougher to decrypt if you decide to use it in web development, for discord bots it's more than fine.

This version is a new, fast and completely rewritten API, originally by Vixen, which was discontinued.
