#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework import serializers
from users.models import Account, CustomerProfile


class AccountRegistrationSerializer(serializers.ModelSerializer):
    """Serializer which handles registration logic."""
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        """Specify json serialization of an account"""
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self, req):
        """Create a new user from registration endpoint."""
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        # check that passwords are equivalent and that the email is unique
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        if len(Account.objects.filter(email=self.validated_data['email'])) > 0:
            raise serializers.ValidationError({'email': 'Email is already in use.'})

        # finalize & save Account object
        account.set_password(password)
        account.save()

        # init & save CustomerProfile
        customer_profile = CustomerProfile(cents=100000, user=account)
        customer_profile.save()

        return account
