import requests

url = "https://jsonplaceholder.typicode.com/users"

new_post = {
    "name": "Kfir",
    "username": "kfir20",
    "email": "kfir@example.com"
}

heders = {"content-Type": "appliction/json"}

respons = requests.post(url, json=new_post, headers=heders)

print(f"{respons.status_code=}")
print(f"{respons.json()}")