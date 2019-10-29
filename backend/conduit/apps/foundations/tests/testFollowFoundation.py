import json
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from ..models import Foundation
from ..serializers import FoundationSerializer


class ProfileFollowAPIViewTestCase(APITestCase):
    foundation_name = 'davinciFoundation'
    createUrl = reverse("foundations:foundations-list")
    url = reverse("foundations:follow", kwargs={'name': foundation_name})

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'davinci', 'davinci@mail.com', 'password')
        self.foundation = {
            'foundation': {
                'name': self.foundation_name,
                'description': 'an amazing foundation'
            }
        }
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.createFoundation(self.foundation)

    def createFoundation(self, foundation):
        response = self.client.post(
            self.createUrl,
            json.dumps(self.foundation),
            content_type='application/json')
        self.assertEqual(201, response.status_code)
        return response

    def getFollowerCount(self):
        response = self.client.get(
            self.createUrl + '/{}'.format(self.foundation_name))
        body = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        return body["foundation"]["followersCount"]

    def test_follow_foundations(self):
        response = self.client.post(self.url)
        self.assertEqual(201, response.status_code)

        # get the count of following and verify it is one
        new_follower_count = self.getFollowerCount()
        self.assertEqual(1, new_follower_count)

    def test_unfollow_foundations(self):
        initial_follower_count = self.getFollowerCount()

        # add a follower
        self.test_follow_foundations()

        # unfollow
        response = self.client.delete(self.url)
        self.assertEqual(200, response.status_code)

        # get the count of following and verify it is one
        new_follower_count = self.getFollowerCount()
        self.assertEqual(initial_follower_count, new_follower_count)
