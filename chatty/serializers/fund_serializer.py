#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from rest_framework import serializers
from chatty.models import Fund


class FundSerializer(serializers.ModelSerializer):
    """
    This class breaks a Fund object into JSON.
    """
    class Meta:
        model = Fund
        fields = ['name', 'id']
