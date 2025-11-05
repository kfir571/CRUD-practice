import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")

print(response.json()[0].keys())

users = response.json()

for i, user in enumerate(users, start=1):
    print(f"{i}. {user['username']} - {user['email']}")