import requests

url = "https://jsonplaceholder.typicode.com/posts/2"

respons = requests.get(url)

update_all_post = respons.json()

update_all_post['title'] = "new title"
update_all_post['body'] = "new budy"

respons = requests.put(url=url, json=update_all_post)
print(respons.status_code)
print(respons.json())

update_part_post = {
    "title": "new title 2",
    "body": "new body 2"
}

respons = requests.patch(url=url, json=update_part_post)

print(respons.status_code)
print(respons.json())