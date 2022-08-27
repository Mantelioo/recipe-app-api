"""Django admin modifications tests"""

import email
from http import client
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):

    # Method is created with a different convention
    # Not really sure why
    # This method will be called before each test
    def setUp(self):
        self.client = Client()
        # Superuser
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="testpass1234",
        )
        self.client.force_login(self.admin_user)
        # Regular user
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass1234",
            name="Test User",
        )

    def test_users_list(self):
        """Test that users are listed on the page"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test user page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)