import requests

response = requests.get('https://ammarsysdev.pythonanywhere.com/api/img').json()

print(response)