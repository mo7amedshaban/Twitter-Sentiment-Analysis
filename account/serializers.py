from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from account.models import Account


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
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account  # not have password2 in AbstractBaseUser
        fields = ['email', 'username', 'password', 'password2', 'id', 'image', 'phone', 'age']
        extra_kwargs = {
            'password': {'write_only': True}  # password not appear in json responcse
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username = data["username"]
        password = data["password"]
        user = Account.objects.get(username=username)
        if user:
            if not user.check_password(data["password"]):
                raise serializers.ValidationError("Incoreect Password")
            return data
        raise serializers.ValidationError("User Not Found")
