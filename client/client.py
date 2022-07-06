import requests

API_KEY = '21f9cbba3a6aeb488e7689ac612e079f458d52df'

headers = {
    'Authorization': 'Token ' + API_KEY,
}

data = {
    "products": ['sadfsdf', 'sadfasdfdsaf']
}

response = requests.put(
    'http://127.0.0.1:8000/promobot/products/1', headers=headers, json=data)

print(response.json())
