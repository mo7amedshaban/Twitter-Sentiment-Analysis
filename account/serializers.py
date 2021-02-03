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
