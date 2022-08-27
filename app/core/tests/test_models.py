"""Tests for user models"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "test1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for the new users."""
        sample_emails = [
            ["test1@EXAMPLE.COM", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        # Validating emails
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample1234")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Should raise ValueError if email is not provided"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test1234")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser("test@example.com", "test1234")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
