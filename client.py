import requests


response = requests.get('http://localhost:8000/item/all')
print(response.status_code)
items = response.json()
print('Items: ', items)
for item in items:
    print("Nome do item é : ", item['nome'])
