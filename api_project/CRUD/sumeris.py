import requests

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

users = response.json()

print(users[0].keys())

for user in users:
    print(f"{user['username']=}, {user['email']=}")

new_user = {
    "name" : "kfir",
    "username": "kf23",
    "email":  "kfir@exmpl.com"
}

response = requests.post(url=url, json=new_user)
print(f"After POST{response.status_code=}")
if response.status_code in range(200,300):
    print(f"{response.json().get('id')=}")


new_url = url + "/" + str(response.json()['id'])

print(new_url)

new_user["name"] = "Kfir"
new_user["email"] = "Kfir@update.com"
response = requests.put(url=new_url, json=new_user)
print(f"after PUT \n{response.status_code=}")

response = requests.delete(url=new_url)
print(f"{response.status_code=}")

requests.exceptions.Timeout
requests.exceptions.ConnectionError
requests.exceptions.HTTPError 