@echo off
set /p id="This will clone the GitHub repository, install the requirements and run the webapp, to proceed type YES elsewise, close the window."
git clone https://github.com/ammarsys/captchaAPI/
cd captchaapi
py -m pip install -r requirements.txt
py app.py