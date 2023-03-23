"""
All the tests about the models
"""
from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from core.models import Ingredient, Review


class UserModelTests(TestCase):
    """Tests about the user model"""

    def test_create_new_user_with_email_password_success(self):
        """Test that creating a new user with email and password is successful"""
        email = "test@example.com"
        password = "123Pass!"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_create_new_user_with_email_username_password(self):
        email = "test@example.com"
        password = "123Pass!"
        username = "test.user"
        user = get_user_model().objects.create_user(
            email=email, password=password, username=username
        )
        self.assertEqual(email, user.email)
        self.assertEqual(username, user.username)
        self.assertTrue(user.check_password(password))

    def test_email_is_normalised(self):
        """Check the email is normalised. Some, although few, providers are case=-sensitive on the first part of the email, so that should stay untouched"""
        emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in emails:
            user = get_user_model().objects.create_user(email, "pass123")
            self.assertEqual(user.email, expected)

    def test_create_user_without_email_fail(self):
        password = "123Pass!"
        username = "test.user"

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email="", password=password, username=username
            )

    def test_create_superuser(self):
        email = "test@example.com"
        password = "Pass123!"
        user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)

    def test_create_superuser_without_password_fails(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser("email@example.com", "")

class RecipeRelatedModelTest(TestCase):
    
    def test_create_new_ingredient(self):
        iname = "pasta"
        ingredient = Ingredient.objects.create(name=iname)
        
        self.assertEqual(str(ingredient), iname)

    def test_create_new_review(self):
        user = get_user_model().objects.create_user(email="test@example.com", password="123456")
        rtitle = "pasta"
        review = Review.objects.create(
            title = rtitle,
            body = "lorem ipsum blah blah",
            rating = 5,
            user = user,
        )
        
        self.assertEqual(str(review), rtitle)
