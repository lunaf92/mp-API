"""
All the tests about the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("users:create")


class PublicApiEndpoints(TestCase):
    def test_user_is_created(self):
        pass

    def test_create_user_with_existing_email_field(self):
        pass

    def test_create_user_with_invalid_email_fail(self):
        pass

    def test_create_user_with_short_password_fail(self):
        pass

    def test_create_user_with_easy_password_fail(self):
        pass

    def test_create_user_with_no_pasword_fail(self):
        pass
