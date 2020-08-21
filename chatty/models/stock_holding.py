#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.db import models
from .fund import Fund


class StockHolding(models.Model):
    """
    Represents a position taken in an asset.
    """

    ticker = models.CharField('The symbol of the stock', max_length=10)
    price_cents = models.IntegerField("Price (in cents) stock is bought at")
    quantity = models.IntegerField("Number of stocks bought")
    fund = models.ForeignKey(Fund, related_name='fund', on_delete=models.SET_NULL, null=True)
    purchased_at = models.DateTimeField('Date and time the asset was purchased', auto_now_add=True)
    sold_at = models.DateTimeField('When asset was sold', null=True)

    @property
    def value(self):
        """
        Returns total value of the stock holding
        :return: Float
        """
        return self.price * self.quantity

    @property
    def price(self):
        """
        Returns the price an asset was bought at in dollars.
        :return: Float
        """
        return self.price_cents * 100
