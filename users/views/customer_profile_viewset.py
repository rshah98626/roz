from ..models import CustomerProfile
from rest_framework import viewsets
from ..serializers import CustomerProfileSerializer


class CustomerProfileViewset(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
