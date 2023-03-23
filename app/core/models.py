from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_args):
        if not email:
            raise ValueError("User must provide a valid email address")
        if not password:
            raise ValueError("User must provide a password")
        user = self.model(email=self.normalize_email(email), **extra_args)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password, **extra_args):
        if not email:
            raise ValueError("User must provide a valid email address")
        if not password:
            raise ValueError("User must provide a password")
        user = self.create_user(email, password, **extra_args)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    first_name = models.CharField(_("Name"), max_length=50, null=True)
    last_name = models.CharField(_("Surname"), max_length=50, null=True)
    username = models.CharField(_("Username"), max_length=50, null=True)
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_active = models.BooleanField(_("Active"), default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

class Ingredient(models.Model):
    name = models.CharField(_("Ingredient"), max_length=50)

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")

    def __str__(self):
        return self.name

class Review(models.Model):

    title = models.CharField(_("Title"), max_length=140)
    body = models.TextField(_("Body"))
    rating = models.IntegerField(_("Rating 1-5"))
    user = models.ManyToManyField(User, verbose_name=_("Author"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return self.title

class Tag(models.Model):

    name = models.CharField(_("Tag name"), max_length=50)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name

class Recipe(models.Model):
    
    class DifficultyChoices(models.TextChoices):
        EASY = '1', 'Easy'
        INTERMEDIATE = '2', 'Intermediate'
        HARD = '3', 'Hard'

    title = models.CharField(_("Recipe name"), max_length=50)
    description = models.TextField(_("Brief description"))
    # photo for later implementation
    difficulty = models.CharField(max_length=1, choices=DifficultyChoices.choices, default=DifficultyChoices.EASY)
    instruction = models.TextField(_("Detailed instructions")),
    time = models.IntegerField(_("Time in minutes")),
    public = models.BooleanField(_("Is Public"), default=False),
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, verbose_name=_("Ingredients"))
    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"))
    reviews = models.ManyToManyField(Review, verbose_name=_("Reviews"))

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")

    def __str__(self):
        return self.title

