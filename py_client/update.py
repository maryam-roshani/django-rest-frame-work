import requests


endpoint = "http://localhost:8000/api/products/10/update/"

data = {
	"title" : "there is problems in here!",
	"content" : "updated content" ,
	"price" : 88
}
get_response = requests.put(endpoint, json=data)

print(get_response.json())
