import requests

api_url = "https://dog.ceo/api/breeds/image/random"

response = requests.get(api_url)

status_code = response.status_code
print(f"Status code: {status_code}")

response_json = response.json()
print(response_json)