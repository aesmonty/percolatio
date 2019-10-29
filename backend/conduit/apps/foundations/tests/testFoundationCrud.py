import json
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from conduit.apps.foundations.models import Foundation
from ..serializers import FoundationSerializer


class FoundationViewSetTestCase(APITestCase):
    url = reverse("foundations:foundations-list")
    listUrl = reverse("foundations:foundationFeed")

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'davinci', 'davinci@mail.com', 'password')
        self.foundation_name = 'davinciFoundation'
        self.client = APIClient()
        self.client.force_authenticate(self.user)

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
        foundation = {
            'foundation': {
                'name': self.foundation_name + "-create",
                'description': 'an amazing foundation'
            }
        }
        self.createFoundation(foundation)

    def test_list_foundation(self):
        response = self.client.get(self.listUrl)
        self.assertEqual(200, response.status_code)

    def test_retrieve_foundations(self):

        test_foundation_name = self.foundation_name + "-retrieve"
        foundation = {
            'foundation': {
                'name': test_foundation_name,
                'description': 'an amazing foundation'
            }
        }
        self.createFoundation(foundation)

        response = self.client.get(
            self.url + '/{}'.format(test_foundation_name))
        self.assertEqual(200, response.status_code)
        self.assertEqual(test_foundation_name, json.loads(
            response.content)["foundation"]["name"])

    def test_update_foundation_authorized(self):
        test_foundation_name = self.foundation_name + "-put"
        foundation = {
            'foundation': {
                'name': test_foundation_name,
                'description': 'an amazing foundation'
            }
        }

        self.createFoundation(foundation)
        new_foundation_name = 'daliFoundation'
        new_foundation = {
            'foundation': {
                'name': new_foundation_name,
                'description': 'an amazing foundation'
            }
        }

        response = self.client.put(
            self.url + '/{}'.format(test_foundation_name),
            json.dumps(new_foundation),
            content_type='application/json')

        self.assertEqual(200, response.status_code)

    def test_update_foundation_unauthorized(self):

        test_foundation_name = self.foundation_name + "-update-unauth"
        # Create other user which is authorized
        otherUser = get_user_model().objects.create_user(
            'mal', 'mal@mail.com', 'password')
        otherClient = APIClient()
        otherClient.credentials(
            HTTP_AUTHORIZATION='Token ' + otherUser.token)

        # Create a foundation as a default user
        foundation = {
            'foundation': {
                'name': test_foundation_name,
                'description': 'an amazing foundation'
            }
        }

        self.createFoundation(foundation)

        # Edit the foundation from another account
        new_foundation_name = 'daliFoundation'
        new_foundation = {
            'foundation': {
                'name': new_foundation_name,
                'description': 'an amazing foundation'
            }
        }

        response = otherClient.put(
            self.url + '/{}'.format(test_foundation_name),
            json.dumps(new_foundation),
            content_type='application/json')

        self.assertEqual(403, response.status_code)
