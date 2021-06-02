from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from account.models import Account
from rest_framework.validators import UniqueValidator

import sys
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class ChangePasswordSerializer(serializers.Serializer):
    model = Account

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class AccountSerializer(serializers.ModelSerializer):
    # add field
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account  # not have password2 in AbstractBaseUser
        fields = ['email', 'username', 'password', 'password2', 'id', 'image', 'phone', 'age']
        extra_kwargs = {
            'password': {'write_only': True}  # password not appear in json responcse
        }

    def save(self):
        account = Account(email=self.validated_data['email'],
                          username=self.validated_data['username'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'not match'})
        account.set_password(password)  # set_password object from Account
        account.save()  # save object from Account
        return account


class UpdateAccountSerializer(serializers.ModelSerializer):
    # add field
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account  # not have password2 in AbstractBaseUser
        fields = ['email', 'username', 'id', 'image', 'phone', 'age']
        # extra_kwargs = {
        #     'password': {'write_only': True}  # password not appear in json responcse
        # }

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         if attr == 'password':
    #             instance.set_password(value)
    #         else:
    #             setattr(instance, attr, value)
    #     instance.save()
    #     return instance


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        user = Account.objects.filter(email=value)
        if not user:
            raise serializers.ValidationError("Wrong Email !!")
        return value

    def validate_password(self, value):
        user = Account.objects.filter(password=value)
        if not user:
            raise serializers.ValidationError("Wrong password !!")
        return value

    # try:
    #     validators.validate_password(value)
    # except exceptions.ValidationError as exc:
    #     raise serializers.ValidationError(str(exc))
    # return value
