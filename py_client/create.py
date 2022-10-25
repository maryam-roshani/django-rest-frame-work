import requests


headers = {'Authorization': 'Bearer fe8cca4849747fc117324edb7ae0a8711493e56c'}
endpoint = "http://localhost:8000/api/products/"

data = {
	"title":"this is done"
}

get_response = requests.post(endpoint, json=data, headers=headers)

print(get_response.json())
