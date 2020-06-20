"""Copyright 2020."""

from django.db import models
from django.contrib.auth import get_user_model


class CustomerProfile(models.Model):
    """
    A CustomerProfile is linked to a User model.

    Specifies other information about the user. This is only for customers.
    """

    cents = models.IntegerField("money in the account", default=0)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def get_money(self):
        """Return the amount of money in a customer's account in dollars."""
        return self.cents / 100
