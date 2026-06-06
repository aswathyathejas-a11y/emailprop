from rest_framework import serializers
from .models import Customer

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer

        fields = [
            'username',
            'email',
            'password'
        ]