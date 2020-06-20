from rest_framework import serializers
from .models import CustomerProfile
from users.serializers import AccountSerializer


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = AccountSerializer(CustomerProfile.user)
    
    class Meta:
        model = CustomerProfile
        fields = ['cents', 'user']
        depth = 1
