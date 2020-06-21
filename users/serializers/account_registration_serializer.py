from rest_framework import serializers
from ..models import Account


class AccountRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self, req):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        if len(Account.objects.filter(email=self.validated_data['email'])) > 0:
            raise serializers.ValidationError({'email': 'Email is already in use.'})
        account.set_password(password)
        account.save()
        return account
