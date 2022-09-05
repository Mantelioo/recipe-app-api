"""
Serializers for the user API view
"""
from dataclasses import field
from pyexpat import model
from django.contrib.auth import get_user_model

from rest_framework import serializers


# Serializer converts object to the Python object or a model
# Json to python for example


class UserSerializer(serializers.ModelSerializer):

    # Model and fields that we want to pass to serializer
    class Meta:
        model = get_user_model()
        field = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)
