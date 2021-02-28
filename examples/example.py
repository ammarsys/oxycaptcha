import requests

response = requests.get('ammarsysdev.pythonanywhere.com/api/img').json()

print(response["link"], response["solution"])
