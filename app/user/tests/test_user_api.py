import email
import imp
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests the public features of API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        # We are checking if the password matches with the one in the DB
        self.assertTrue(user.check_password(payload["password"]))

        # We need to make sure that user won't receive a password hash (security)
        # Checking the test if user does not recieve a password
        self.assertNotIn("password", res.data)  # no password key is returned from API

    def test_user_with_email_exists_error(self):
        """Error returned if user with email exists (already in DB)"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test name",
        }

        create_user(**payload)  # email = "", password = ""
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Error if pass is less than 5 chars"""
        payload = {
            "email": "test@example.com",
            "password": "pw",
            "name": "Test name",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)
