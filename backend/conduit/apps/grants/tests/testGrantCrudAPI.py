import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from conduit.apps.foundations.models import Foundation
from conduit.apps.profiles.models import Profile

from .common import getGrantBasic, getGrantComplete, fake


class GrantsViewSetTestCase(APITestCase):
    url = reverse("grants:grants-list")

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            fake.user_name(),
            fake.email(),
            fake.text(max_nb_chars=14))
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        self.foundation_name = fake.company()
        self.foundation = Foundation.objects.create(
            founder=self.user.profile,
            name=self.foundation_name,
            description=fake.paragraph())

        otherUser = get_user_model().objects.create_user(
            fake.user_name(),
            fake.email(),
            fake.text(max_nb_chars=14))
        self.otherClient = APIClient()
        self.otherClient.credentials(
            HTTP_AUTHORIZATION='Token ' + otherUser.token)

    def create_grant(self, grant):
        response = self.client.post(
            self.url,
            json.dumps(grant),
            content_type='application/json')
        self.assertEqual(201, response.status_code)
        return response

    def test_create_grant(self):
        self.create_grant(getGrantBasic(self.foundation_name))
        self.create_grant(getGrantComplete(self.foundation_name))

    def test_create_grant_unauthorized(self):
        response = self.otherClient.post(
            self.url,
            json.dumps(getGrantComplete(self.foundation_name)),
            content_type='application/json')
        self.assertEqual(403, response.status_code)

    def test_update_grant(self):
        response = self.create_grant(getGrantComplete(self.foundation_name))
        slug = json.loads(response.content)["grant"]["slug"]
        expected_title = fake.company()

        response = self.client.put(
            self.url + '/{}'.format(slug),
            data=json.dumps({
                "Grant": {
                    "title": expected_title,
                }
            }),
            content_type='application/json')

        self.assertEqual(200, response.status_code)
        new_title = json.loads(response.content)["grant"]["title"]
        self.assertEqual(expected_title, new_title)

    def test_update_grant_unauthorized(self):
        response = self.create_grant(getGrantComplete(self.foundation_name))
        slug = json.loads(response.content)["grant"]["slug"]

        response = self.otherClient.put(
            self.url + '/{}'.format(slug),
            data=json.dumps({
                "Grant": {
                    "title": fake.company(),
                }
            }),
            content_type='application/json')
        self.assertEqual(403, response.status_code)

    def test_delete_grant(self):
        response = self.create_grant(getGrantComplete(self.foundation_name))
        slug = json.loads(response.content)["grant"]["slug"]
        response = self.client.delete(self.url + '/{}'.format(slug))
        self.assertEqual(200, response.status_code)

    def test_delete_grant_unauthorized(self):
        response = self.create_grant(getGrantComplete(self.foundation_name))
        slug = json.loads(response.content)["grant"]["slug"]

        response = self.otherClient.delete(self.url + '/{}'.format(slug))
        self.assertEqual(403, response.status_code)

    def test_list_grant(self):
        numberOfGrants = 10
        for _ in range(0, numberOfGrants):
            self.create_grant(getGrantComplete(self.foundation_name))

        response = self.client.get(
            self.url)
        self.assertEqual(200, response.status_code)
        grantCount = json.loads(response.content)["grantsCount"]
        self.assertEqual(numberOfGrants, grantCount)

    def test_get_grant(self):
        response = self.create_grant(getGrantComplete(self.foundation_name))
        slug = json.loads(response.content)["grant"]["slug"]
        response = self.client.get(self.url + '/{}'.format(slug))
        self.assertEqual(200, response.status_code)
