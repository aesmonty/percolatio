import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from conduit.apps.foundations.models import Foundation
from conduit.apps.profiles.models import Profile

from .commonObjects import getTestGrant


class ApplicantsListAPIViewTestCase(APITestCase):
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

        self.grant = getTestGrant(self.foundation_name)

        self.application = {
            "application": {
                "body": "this is why I am applying to this grant"
            }
        }

        self.make_mal_client()

    def make_mal_client(self):
        # create a mal user
        self.otherUser = get_user_model().objects.create_user(
            'mal', 'mal@mail.com', 'password')
        self.otherClient = APIClient()
        self.otherClient.credentials(
            HTTP_AUTHORIZATION='Token ' + self.otherUser.token)

    def create_grant(self):
        response = self.client.post(
            self.createUrl,
            json.dumps(self.grant),
            content_type='application/json')
        self.assertEqual(201, response.status_code)
        return response

    def create_application(self, slug):
        response = self.client.post(
            reverse("grants:applicationCreate", kwargs={'grantSlug': slug}),
            json.dumps(self.application),
            content_type='application/json')
        self.assertEqual(201, response.status_code)
        return response

    def test_create_application(self):
        response = self.create_grant()
        slug = json.loads(response.content)["grant"]["slug"]
        response = self.create_application(slug)
        applicationId = json.loads(response.content)["id"]
        response = self.client.get(
            reverse("grants:applicationCreate", kwargs={'grantSlug': slug})
        )
        self.assertEqual(200, response.status_code)
        responseId = json.loads(response.content)["results"][0]["id"]
        self.assertEqual(applicationId, responseId)

    def test_list_applications_authorized(self):
        response = self.create_grant()
        slug = json.loads(response.content)["grant"]["slug"]
        application_number = 10
        for _ in range(0, application_number):
            self.create_application(slug)

        response = self.client.get(
            reverse("grants:applicationCreate", kwargs={'grantSlug': slug})
        )
        self.assertEqual(200, response.status_code)
        application_count_returned = json.loads(response.content)["count"]
        self.assertEqual(application_number, application_count_returned)

    def test_list_applications_unauth(self):
        response = self.create_grant()
        slug = json.loads(response.content)["grant"]["slug"]

        response = self.otherClient.get(
            reverse("grants:applicationCreate", kwargs={'grantSlug': slug})
        )
        self.assertEqual(403, response.status_code)

    def test_destroy_application(self):
        response = self.create_grant()
        slug = json.loads(response.content)["grant"]["slug"]
        response = self.create_application(slug)
        applicationId = json.loads(response.content)["id"]
        response = self.client.delete(
            reverse("grants:applicationDestroy",
                    kwargs={
                        'grantSlug': slug,
                        'id': applicationId
                    })
        )
        self.assertEqual(204, response.status_code)

    def test_destroy_application_unauth(self):

        # create a grant from the basic user
        response = self.create_grant()
        slug = json.loads(response.content)["grant"]["slug"]
        response = self.create_application(slug)
        applicationId = json.loads(response.content)["id"]

        # try to destroy the grant from the mal user
        response = self.otherClient.delete(
            reverse("grants:applicationDestroy",
                    kwargs={
                        'grantSlug': slug,
                        'id': applicationId
                    })
        )
        self.assertEqual(403, response.status_code)
