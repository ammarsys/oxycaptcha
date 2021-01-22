# Captcha API
I made this API so I can use it alongside https://github.com/Ammar-sys/essentials discord bot and I've decided to make it public. The API is live at https://ammarsysdev.pythonanywhere.com/ . Please let me know if you run into any issues.

# USAGE

## wrappers

 - JavaScript: https://www.npmjs.com/package/essentials-captcha
 - Repository & Creator: https://github.com/SpeckyYT/essentials-captcha#readme

## manual install
 
 Make sure to go through the files and edit paths. (both py files)
 
 To install the necessary modules for this to run do

```
pip install requirements.txt
``` 

Incase that doesn't work, try:

```
py -m pip install requirements.txt
```

It's recommended to run both clean_up.py and main.py. Clean_up.py deletes captchas in the folder in order to save storage

Its intended for discord bots BUT it can be used for web development (if you don't really care about good security) and other projects as the image has basic encryption. You may want to make it a bit more tougher to decrypt if you decide to use it in web development, for discord bots it's more than fine.

This version is a new, fast and completely rewritten API, originally by Vixen, which was discontinued.
