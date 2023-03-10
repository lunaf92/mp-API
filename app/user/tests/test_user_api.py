"""
All the tests about the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")


def create_user(email="test@example.com", password="45Egd!!94"):
    return get_user_model().objects.create_user(email, password)


class PublicApiEndpoints(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_user_is_created(self):
        payload = {
            "email": "test@example.com",
            "username": "test.user",
            "password": "45Egd!!94",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertIn(res.data, payload["email"])
        self.assertIn(res.data, payload["username"])
        self.assertNotIn(res.data, payload["password"])

    def test_create_user_with_existing_email_field(self):
        create_user()
        payload = {
            "email": "test@example.com",
            "username": "test.user",
            "password": "45Egd!!94",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_invalid_email_fail(self):
        payload = {
            "email": "test.example.com",
            "username": "test.user",
            "password": "45Egd!!94",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_password_fail(self):
        payload = {
            "email": "test@example.com",
            "username": "test.user",
            "password": "4",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_easy_password_fail(self):
        payload = {
            "email": "test@example.com",
            "username": "test.user",
            "password": "123456789",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_pasword_fail(self):
        payload = {"email": "test@example.com", "username": "test.user", "password": ""}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
