from rest_framework import serializers
from .models import Customer,Product,RecentSearch,Cart


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer

        fields = [
            'username',
            'email',
            'password'
        ]

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        exclude = ['password']

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
class RecentSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecentSearch
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = '__all__'