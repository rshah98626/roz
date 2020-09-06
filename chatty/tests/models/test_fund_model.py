#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from chatty.models import Fund, StockHolding, Post


class FundModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fund = Fund(
            cash_on_hand_cents=1000
        )
        fund.save()

        # init stock holdings
        apple_stock = StockHolding(
            ticker='AAPL',
            price_cents=50000,
            quantity=10,
            fund=fund
        )
        apple_stock.save()

        tesla_stock = StockHolding(
            ticker='TSLA',
            price_cents=100000,
            quantity=5,
            fund=fund
        )
        tesla_stock.save()

        # init posts
        post1 = Post(
            message='We\'re buying Tesla today guys! 2000 is a lucky number.',
            fund=fund
        )
        post1.save()

        post2 = Post(
            message='When you can\'t beat \'em, join \'em.',
            fund=fund
        )
        post2.save()

    def test_cash_in_dollars(self):
        self.assertEqual(Fund.objects.latest('id').cash, 10)

    def test_total_value(self):
        self.assertEqual(Fund.objects.latest('id').total_value, 10010)

    def test_stock_holdings(self):
        fund = Fund.objects.latest('id')
        self.assertEqual(len(fund.holdings.all()), 2)
        apple = fund.holdings.first()
        tesla = fund.holdings.last()

        # test apple
        self.assertEqual(apple.ticker, 'AAPL')
        self.assertEqual(apple.price_cents, 50000)
        self.assertEqual(apple.quantity, 10)

        # test tesla
        self.assertEqual(tesla.ticker, 'TSLA')
        self.assertEqual(tesla.price_cents, 100000)
        self.assertEqual(tesla.quantity, 5)

    def test_posts(self):
        fund = Fund.objects.latest('id')
        self.assertEqual(len(fund.posts.all()), 2)
        self.assertEqual(fund.posts.first().message, 'We\'re buying Tesla today guys! 2000 is a lucky number.')
        self.assertEqual(fund.posts.last().message, 'When you can\'t beat \'em, join \'em.')

    def test_field_labels(self):
        fund = Fund.objects.latest('id')
        self.assertEquals(fund._meta.get_field('cash_on_hand_cents').verbose_name, 'Money not in investments (cents)')

    def test_cash_cents_is_correct(self):
        self.assertEqual(Fund.objects.latest('id').cash_on_hand_cents, 1000)
