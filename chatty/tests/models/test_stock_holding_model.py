#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from chatty.models import StockHolding, Fund
from datetime import datetime, timezone


class StockHoldingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fund = Fund(cash_on_hand_cents=0)
        fund.save()

        cls.ticker = 'AAPL'
        cls.price_cents = 10000
        cls.quantity = 10

        cls.before_purchased = datetime.now(timezone.utc)
        stock_holding = StockHolding(
            ticker=cls.ticker,
            price_cents=cls.price_cents,
            quantity=cls.quantity,
            fund=fund
        )
        stock_holding.save()

        cls.before_sold = datetime.now(timezone.utc)
        stock_holding.sold_at = datetime.now(timezone.utc)
        stock_holding.save()

    def test_price_cents(self):
        self.assertEqual(StockHolding.objects.latest('id').price_cents, self.price_cents)

    def test_ticker(self):
        self.assertEqual(StockHolding.objects.latest('id').ticker, self.ticker)

    def test_quantity(self):
        self.assertEqual(StockHolding.objects.latest('id').quantity, self.quantity)

    def test_fund(self):
        self.assertEqual(StockHolding.objects.latest('id').fund, Fund.objects.latest('id'))

    def test_purchased_at(self):
        self.assertGreater(StockHolding.objects.latest('id').purchased_at, self.before_purchased)

    def test_sold_at(self):
        self.assertGreater(StockHolding.objects.latest('id').sold_at, self.before_sold)

    def test_field_labels(self):
        stock_holding = StockHolding.objects.latest('id')
        self.assertEqual(stock_holding._meta.get_field('ticker').verbose_name, 'The symbol of the stock')
        self.assertEqual(stock_holding._meta.get_field('price_cents').verbose_name,
                          'Price (in cents) stock is bought at')
        self.assertEqual(stock_holding._meta.get_field('quantity').verbose_name, 'Number of stocks bought')
        self.assertEqual(stock_holding._meta.get_field('fund').verbose_name, 'fund')
        self.assertEqual(stock_holding._meta.get_field('purchased_at').verbose_name,
                          'Date and time the asset was purchased')
        self.assertEqual(stock_holding._meta.get_field('sold_at').verbose_name, 'When asset was sold')

    def test_value_property(self):
        value = self.price_cents * self.quantity / 100
        self.assertEqual(StockHolding.objects.latest('id').value, value)

    def test_price_property(self):
        price = self.price_cents / 100
        self.assertEqual(StockHolding.objects.latest('id').price, price)
