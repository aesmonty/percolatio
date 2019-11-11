import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from conduit.apps.foundations.models import Foundation
from conduit.apps.profiles.models import Profile


class GrantsFavoriteAPIViewTestCase(APITestCase):
    createUrl = reverse("grants:grants-list")

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

        self.application = {
            "application": {
                "body": "this is why I am applying to this grant"
            }
        }

    def create_grant(self):
        response = self.client.post(
            self.createUrl,
            json.dumps(self.grant),
            content_type='application/json')
        self.assertEqual(201, response.status_code)
        return response

    def favorite_application(self, slug):
        response = self.client.post(
            reverse("grants:grantFavorite", kwargs={'grantSlug': slug}),
            json.dumps(self.application),
            content_type='application/json')
        self.assertEqual(201, response.status_code)
        return response

    def test_favorite_application(self):
        response = self.create_grant()
        slug = json.loads(response.content)["grant"]["slug"]
        self.favorite_application(slug)

    def test_unfavorite_application(self):
        response = self.create_grant()
        slug = json.loads(response.content)["grant"]["slug"]
        response = self.favorite_application(slug)

        response = self.client.delete(
            reverse("grants:grantFavorite",
                    kwargs={
                        'grantSlug': slug
                    })
        )
        self.assertEqual(200, response.status_code)
