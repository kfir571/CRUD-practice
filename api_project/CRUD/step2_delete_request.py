import requests

def print_respons(respons):
    print(respons.status_code)
    print(respons.text)


url = "https://jsonplaceholder.typicode.com/posts/3"

respons = requests.delete(url)
print("-----DELETE-----")
print_respons(respons)

respons = requests.get(url)

print("-----GET-----")
print_respons(respons)
