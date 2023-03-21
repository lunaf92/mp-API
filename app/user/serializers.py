from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "last_name", "username", "password"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = self.Meta.model(**data)

        # get the password from the data
        password = data.get("password")

        errors = dict()
        try:
            # validate the password and catch the exception
            validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)
