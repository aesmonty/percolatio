import requests
import json

import argparse

parser = argparse.ArgumentParser(description='Populates percolatio db')
parser.add_argument('-u','--username', help='User name', required=True)
parser.add_argument('-p','--password', help='User password', required=True)
parser.add_argument('-e','--email', help='User email', required=True)
parser.add_argument('-z','--url', help='User email', required=False, default = "http://127.0.0.1:8000/api/")


args = parser.parse_args()

# url = "http://percdev.eu-west-1.elasticbeanstalk.com/api/"

username = args.username
password = args.password
email = args.email
url = args.url
user = {
    "user":
    {
        "email": email,
        "password": password,
        "username": username,
    }
}

print("Sing-up user with name {}".format(username))

create_user_endpoint = "users"
r = requests.post("{}{}".format(url, create_user_endpoint),
                    data=json.dumps(user),
                    headers={"content-type": "application/json"})

login_user_endpoint = "users/login/"
if r.status_code != 200:
    r = requests.post("{}{}".format(url, login_user_endpoint),
                    data=json.dumps(user),
                    headers={"content-type": "application/json"})

    if r.status_code != 200:
        raise Exception("User login seems to be broken")
    else:
        print("User already exists. Logging in with the user instead.")

token = json.loads(r.content)['user']['token']

get_user_endpoint = "user/"
headers_with_auth = {
    "authorization" : "Token {}".format(token),
    "content-type": "application/json"
}

r = requests.get("{}{}".format(url, get_user_endpoint, username),
                    data=json.dumps(user),
                    headers=headers_with_auth)

print(r.status_code)
print(r.content)