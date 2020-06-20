from rest_framework import viewsets
from .serializers import CustomerProfileSerializer
from .models import CustomerProfile


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
