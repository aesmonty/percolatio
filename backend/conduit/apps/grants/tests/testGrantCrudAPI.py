import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from conduit.apps.foundations.models import Foundation
from conduit.apps.profiles.models import Profile


class GrantsViewSetTestCase(APITestCase):
    url = reverse("grants:grants-list")
    # listUrl = reverse("foundations:foundationFeed")

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'davinci', 'davinci@mail.com', 'password')
        self.foundation_name = 'davinciFoundation'
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.profile = Profile.objects.get(user=self.user)
        self.foundation = Foundation.objects.create(
            founder=self.profile,
            name=self.foundation_name,
            description='foo')

        self.grant = {
            "Foundation": {
                "Name": self.foundation_name
            },
            "Grant": {
                "title": "Test grant is the best",
                "description": "decription",
                "body": "nice body",
                "amount": "10000"
            }
        }

    def create_grant(self):
        response = self.client.post(
            self.url,
            json.dumps(self.grant),
            content_type='application/json')
        self.assertEqual(201, response.status_code)
        return response

    def test_create_grant(self):
        _ = self.create_grant()

    def test_update_grant(self):
        response = self.create_grant()
        slug = json.loads(response.content)["grant"]["slug"]
        expected_title = "bar"
        response = self.client.put(
            self.url + '/{}'.format(slug),
            data=json.dumps({
                "Foundation": {
                    "Name": self.foundation_name
                },
                "Grant": {
                    "title": expected_title,
                }
            }),
            content_type='application/json')

        self.assertEqual(200, response.status_code)
        new_title = json.loads(response.content)["grant"]["title"]
        self.assertEqual(expected_title, new_title)

    # def test_delete_grant(self):
    #     response = self.create_grant()
    #     slug = json.loads(response.content)["grant"]["slug"]
    #     response = self.client.delete(
    #         self.url + '{}'.format(slug),
    #         json.dumps(
    #             {
    #                 "Foundation": {
    #                     "Name": self.foundation_name
    #                 }
    #             }),
    #         content_type='application/json')
    #     self.assertEqual(204, response.status_code)