#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.db import models
from django.contrib.auth import get_user_model


class CustomerProfile(models.Model):
    """
    A CustomerProfile is linked to a User model.

    Specifies other information about the user. This is only for customers.
    """

    cents = models.IntegerField("money in the account (cents)", default=0)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    @property
    def get_dollars(self):
        """Return the amount of money in a customer's account in dollars."""
        return self.cents / 100
