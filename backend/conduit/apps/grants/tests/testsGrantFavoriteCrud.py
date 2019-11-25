import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from conduit.apps.foundations.models import Foundation
from conduit.apps.profiles.models import Profile

from .commonObjects import getGrantBasic, fake


class GrantsFavoriteAPIViewTestCase(APITestCase):
    createUrl = reverse("grants:grants-list")

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

        self.grant = getGrantBasic(self.foundation_name)

    def create_grant(self):
        response = self.client.post(
            self.createUrl,
            json.dumps(self.grant),
            content_type='application/json')
        self.assertEqual(201, response.status_code)
        return response

    def favorite_application(self, slug):
        response = self.client.post(
            reverse("grants:grantFavorite",
                    kwargs={'grantSlug': slug}))
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
