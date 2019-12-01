import json
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from conduit.apps.foundations.models import Foundation
from ..serializers import FoundationSerializer

from .common import getFoundationBasic, getFoundationComplete, fake


class FoundationViewSetTestCase(APITestCase):
    url = reverse("foundations:foundations-list")

    def setUp(self):
        self.user = self.getUser()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def getUser(self):
        return get_user_model().objects.create_user(
            fake.user_name(),
            fake.email(),
            fake.text(max_nb_chars=14))

    def createFoundation(self, foundation):
        response = self.client.post(
            self.url,
            json.dumps(foundation),
            content_type='application/json')
        expected_foundation_name = foundation['foundation']['name']
        self.assertEqual(201, response.status_code)
        self.assertEqual(expected_foundation_name, json.loads(
            response.content)["foundation"]["name"])
        return response

    def test_create_foundation(self):
        self.createFoundation(getFoundationBasic())
        self.createFoundation(getFoundationComplete())

    def test_create_foundation_should_fail_when_name_already_exists(self):
        test_foundation_name = fake.company()
        self.createFoundation(getFoundationBasic(test_foundation_name))
        response = self.client.post(
            self.url,
            json.dumps(getFoundationBasic(test_foundation_name)),
            content_type='application/json')
        self.assertEqual(409, response.status_code)

    def test_list_foundation(self):
        count = 10
        for _ in range(0, count):
            self.createFoundation(getFoundationComplete())

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(count, int(json.loads(
            response.content)["foundationsCount"]))

    def test_retrieve_foundations(self):

        test_foundation_name = fake.company()
        self.createFoundation(getFoundationComplete(test_foundation_name))

        response = self.client.get(
            self.url + '/{}'.format(test_foundation_name))
        self.assertEqual(200, response.status_code)
        self.assertEqual(test_foundation_name, json.loads(
            response.content)["foundation"]["name"])

    def test_update_foundation_authorized(self):
        test_foundation_name = fake.company()
        new_foundation_name = fake.company()
        self.createFoundation(getFoundationComplete(test_foundation_name))

        response = self.client.put(
            self.url + '/{}'.format(test_foundation_name),
            json.dumps(getFoundationComplete(new_foundation_name)),
            content_type='application/json')

        self.assertEqual(200, response.status_code)

    def test_update_foundation_unauthorized(self):

        test_foundation_name = fake.company()
        self.createFoundation(getFoundationComplete(test_foundation_name))

        # Create other user which is not authorized
        otherUser = self.getUser()
        otherClient = APIClient()
        otherClient.credentials(
            HTTP_AUTHORIZATION='Token ' + otherUser.token)

        response = otherClient.put(
            self.url + '/{}'.format(test_foundation_name),
            json.dumps(getFoundationComplete()),
            content_type='application/json')

        self.assertEqual(403, response.status_code)
