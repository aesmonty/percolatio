import requests
import json

from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse
from conduit.apps.foundations.tests.common import getFoundationBasic, getFoundationComplete, fake


class Command(BaseCommand):
    help = 'Populates the percolatio db'

    def add_arguments(self, parser):
        parser.add_argument('-u','--username', help='User name. e.g. sotirisnan', required=True)
        parser.add_argument('-p','--password', help='User password. e.g. password', required=True)
        parser.add_argument('-e','--email', help='User email. e.g. sotiris@percolatio.com', required=True)
        parser.add_argument('-z','--url', help='Endpoint e.g. http://127.0.0.1:8000 or http://percdev.eu-west-1.elasticbeanstalk.com', required=False, default = "http://127.0.0.1:8000")

    def handle(self, *args, **options):
        
        username = options['username']
        password = options['password']
        email = options['email']
        url = options['url']
        user = {
            "user":
            {
                "email": email,
                "password": password,
                "username": username,
            }
        }

        print("Sing-up user with name {}".format(username))

        create_user_endpoint = "/api/users"
        r = requests.post("{}{}".format(url, create_user_endpoint),
                            data=json.dumps(user),
                            headers={"content-type": "application/json"})

        login_user_endpoint = "/api/users/login/"
        if r.status_code != 200:
            r = requests.post("{}{}".format(url, login_user_endpoint),
                            data=json.dumps(user),
                            headers={"content-type": "application/json"})

            if r.status_code != 200:
                raise Exception("User login seems to be broken")
            else:
                print("User already exists. Logging in with the user instead.")

        token = json.loads(r.content)['user']['token']

        get_user_endpoint = "/api/user/"
        headers_with_auth = {
            "authorization" : "Token {}".format(token),
            "content-type": "application/json"
        }

        r = requests.get("{}{}".format(url, get_user_endpoint, username),
                            data=json.dumps(user),
                            headers=headers_with_auth)

        if r.status_code != 200:
            raise Exception("User login seems to be broken")

        print("Creating a foundation for the user")
        r = requests.post("{}{}".format(url, reverse("foundations:foundations-list")),
                    data=json.dumps(getFoundationComplete()),
                    headers=headers_with_auth)

        if r.status_code != 201:
            raise Exception("Creating a foundation seems to be broken")

        print("I created a foundation with the following data:")
        print(json.dumps(json.loads(r.content), indent=4, sort_keys=True))

