#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.db import models


class Fund(models.Model):
    """
    This object represents a group of holdings based around a certain strategy.
    """

    cash_on_hand_cents = models.IntegerField("Money not in investments (cents)", default=0)

    @property
    def cash(self):
        """
        Gets the cash on hand in dollars
        :return: Float
        """
        return self.cash_on_hand_cents * 100

    @property
    def total_value(self):
        """
        Returns the total value of the fund (in dollars) at this point in time.
        :return: Float
        """
        total = sum(holding.value for holding in self.stock_holdings)
        return total + self.cash

    @property
    def stock_holdings(self):
        """
        Returns the stock holdings for a given
        :return: [StockHolding]
        """
        return self.stock_holding_set.all()
