#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.db import models


class Fund(models.Model):
    """
    This object represents a group of holdings based around a certain strategy.
    """
    name = models.CharField('The name of the fund', max_length=100, unique=True)
    cash_on_hand_cents = models.IntegerField(
        "Money not in investments (cents)", default=0)

    @property
    def cash(self):
        """
        Gets the cash on hand in dollars.
        :return: Float
        """
        return self.cash_on_hand_cents / 100

    @property
    def total_value(self):
        """
        Returns the total value of the fund (in dollars) at this point in time.
        :return: Float
        """
        total = sum(holding.value for holding in self.holdings.all())
        return total + self.cash

    def __str__(self):
        return f"{self.name}"
