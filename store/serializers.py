from rest_framework import serializers

from store.models import Product
from django.utils.timezone import now


class ProductSerializer(serializers.ModelSerializer):
    # Add new field to serializer
    username = serializers.SerializerMethodField('username_from_account')

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['slug', 'title', 'description', 'price', 'username']

    # obj = model it self
    def username_from_account(self, obj):
        username = obj.account.username   # here exist relationship between Product 1:m account
        return username
