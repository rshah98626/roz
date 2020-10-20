#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from chatty.models import Fund, StockHolding, Post, Article, Video


class FundModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fund_cash = 1000
        cls.ticker1 = 'AAPL'
        cls.stock_price1 = 50000
        cls.stock_quantity1 = 10
        cls.ticker2 = 'TSLA'
        cls.stock_price2 = 100000
        cls.stock_quantity2 = 5
        cls.post_message1 = 'We\'re buying Tesla today guys! 2000 is a lucky number.'
        cls.post_message2 = 'When you can\'t beat \'em, join \'em.'
        cls.article_message1 = "This is the first article I've written. I recommend you buy $ORNGE because it's going" \
                               " to do well during earnings."
        cls.video_file_name1 = "funny.mp4"

        fund = Fund(
            cash_on_hand_cents=cls.fund_cash
        )
        fund.save()

        # init stock holdings
        apple_stock = StockHolding(
            ticker=cls.ticker1,
            price_cents=cls.stock_price1,
            quantity=cls.stock_quantity1,
            fund=fund
        )
        apple_stock.save()

        tesla_stock = StockHolding(
            ticker=cls.ticker2,
            price_cents=cls.stock_price2,
            quantity=cls.stock_quantity2,
            fund=fund
        )
        tesla_stock.save()

        # init posts
        post1 = Post(
            message=cls.post_message1,
            fund=fund
        )
        post1.save()

        post2 = Post(
            message=cls.post_message2,
            fund=fund
        )
        post2.save()

        # init article
        article1 = Article(
            text=cls.article_message1,
            fund=fund
        )
        article1.save()

        # init video
        video1 = Video(
            file_name=cls.video_file_name1,
            fund=fund
        )
        video1.save()

    def test_cash_in_dollars(self):
        self.assertEqual(Fund.objects.latest('id').cash, self.fund_cash / 100)

    def test_total_value(self):
        value = (self.stock_price1 / 100 * self.stock_quantity1) + (self.stock_price2 / 100 * self.stock_quantity2) + \
                (self.fund_cash / 100)
        self.assertEqual(Fund.objects.latest('id').total_value, value)

    def test_stock_holdings(self):
        fund = Fund.objects.latest('id')
        self.assertEqual(len(fund.holdings.all()), 2)
        apple = fund.holdings.first()
        tesla = fund.holdings.last()

        # test apple
        self.assertEqual(apple.ticker, self.ticker1)
        self.assertEqual(apple.price_cents, self.stock_price1)
        self.assertEqual(apple.quantity, self.stock_quantity1)

        # test tesla
        self.assertEqual(tesla.ticker, self.ticker2)
        self.assertEqual(tesla.price_cents, self.stock_price2)
        self.assertEqual(tesla.quantity, self.stock_quantity2)

    def test_posts(self):
        fund = Fund.objects.latest('id')
        self.assertEqual(len(fund.posts.all()), 2)
        self.assertEqual(fund.posts.first().message, self.post_message1)
        self.assertEqual(fund.posts.last().message, self.post_message2)

    def test_field_labels(self):
        fund = Fund.objects.latest('id')
        self.assertEqual(fund._meta.get_field('cash_on_hand_cents').verbose_name, 'Money not in investments (cents)')

    def test_cash_cents_is_correct(self):
        self.assertEqual(Fund.objects.latest('id').cash_on_hand_cents, self.fund_cash)

    def test_article(self):
        fund = Fund.objects.latest('id')
        self.assertEqual(len(fund.articles.all()), 1)
        self.assertEqual(fund.articles.first().text, self.article_message1)

    def test_video(self):
        fund = Fund.objects.latest('id')
        self.assertEqual(len(fund.videos.all()), 1)
        self.assertEqual(fund.videos.first().file_name, self.video_file_name1)
