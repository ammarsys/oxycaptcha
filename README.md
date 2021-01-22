# Captcha API
I made this API so I can use it alongside https://github.com/Ammar-sys/essentials discord bot and I've decided to make it public. The API is live at https://ammarsysdev.pythonanywhere.com/ . Please let me know if you run into any issues.

# USAGE

## wrappers

 - Typescript: https://www.npmjs.com/package/essentials-captcha
 - Repository & Creator: https://github.com/SpeckyYT/essentials-captcha#readme

## manual install

To keep whatever you're using this for safe you have 2 options:

 - update the images folder each day with around 1k images
 - use a captcha generator ( https://github.com/Ammar-sys/captchagen will work if you configure it correctly)
 
 Make sure to go through the files and edit paths.
 
 To install the necessary modules for this to run do

```
pip install requirements.txt
``` 

Incase that doesn't work, try:

```
py -m pip install requirements.txt
```

Its intended for discord bots BUT it can be used for web development (if you don't really care about the security) and other projects as the image has basic encryption solution. You may want to make it a bit more tougher to decrypt if you decide to use it. (ex: reversing the string, hex/binary/other stuff encryption, ...)

This version is a new, fast and completely rewritten API, originally by Vixen, which was discontinued.
