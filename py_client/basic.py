import requests


endpoint = "http://localhost:8000/api/?abc=123"

get_response = requests.post(endpoint, json={"title":"lemon", "content":"Another Fruit"})

print(get_response.json())
