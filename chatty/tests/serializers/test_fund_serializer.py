#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

from django.test import TestCase
from chatty.serializers import FundSerializer
from chatty.models import Fund


class FundSerializerTest(TestCase):
    def test_fund_deserialization(self):
        """
        Verify that a request is a valid serialization of Fund.
        :return:
        """
        serializer = FundSerializer(data={
            'name': 'Fundy'
        })
        self.assertTrue(serializer.is_valid())

    def test_fund_serialization(self):
        """
        Make sure that a Fund is represented in JSON correctly.
        :return:
        """
        fund_name = 'Fundy'
        f = Fund.objects.create(cash_on_hand_cents=0, name=fund_name)

        serialized_data = FundSerializer(f).data

        self.assertEqual(serialized_data['name'], fund_name)
        self.assertEqual(serialized_data['id'], f.id)
