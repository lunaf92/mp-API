"""
All the tests about the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
SELF_URL = reverse("user:self")


def create_user(email="test@example.com", password="45Egd!!94", **kwargs):
    return get_user_model().objects.create_user(email, password, **kwargs)


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
        self.assertIn(payload["email"], res.data.values())
        self.assertIn(payload["username"], res.data.values())
        self.assertNotIn(payload["password"], res.data.values())
        self.assertNotIn("password", res.data.keys())

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

    def test_login_create_token(self):
        payload = {
            "email": "test@example.com",
            "username": "test.user",
            "password": "45Egd!!94",
        }
        create_user(email=payload["email"], password=payload["password"])
        res = self.client.post(
            TOKEN_URL, data={"email": payload["email"], "password": payload["password"]}
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data.keys())

    def test_bad_password_no_token(self):
        create_user()
        payload = {
            "email": "test@example.com",
            "password": "badpass",
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data.keys())

    def test_bad_email_no_token(self):
        create_user()
        payload = {
            "email": "notexist@example.com",
            "password": "45Egd!!94",
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data.keys())

    def test_no_password_no_token(self):
        create_user()
        payload = {
            "email": "test@example.com",
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data.keys())

    def test_no_email_no_token(self):
        create_user()
        payload = {
            "password": "45Egd!!94",
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data.keys())

    def test_blank_password_no_token(self):
        create_user()
        payload = {
            "email": "test@example.com",
            "password": "",
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data.keys())

    def test_blank_email_no_token(self):
        create_user()
        payload = {
            "email": "",
            "password": "45Egd!!94",
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data.keys())

    def test_unauthenticated_user_forbidden_access(self):
        res = self.client.get(SELF_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEndpoints(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="federico@example.com",
            password="123!!ABCabc",
            username="federico.lunardon",
            first_name="federico",
            last_name="lunardon",
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_self_page_ok(self):
        res = self.client.get(SELF_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('username', res.data.keys())
        self.assertIn('federico.lunardon', res.data.values())
        self.assertIn('email', res.data.keys())
        self.assertIn('first_name', res.data.keys())
        self.assertIn('last_name', res.data.keys())
        self.assertNotIn('password', res.data.keys())

    def test_post_fails(self):
        res = self.client.post(SELF_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_partial_update_success(self):
        payload = {
            "username": "lunafede92",
            "password": "NewPasw123!!"
        }
        
        self.client.patch(SELF_URL, payload)

        self.user.refresh_from_db()
        
        self.assertEqual(self.user.username, payload["username"])
        self.assertTrue(self.user.check_password(payload["password"]))