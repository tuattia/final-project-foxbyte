from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        extra_kwargs = {
            'password': {'write_only': True},
        }

        fields = (
            'id',
            'name',
            'username',
            'password'
        )