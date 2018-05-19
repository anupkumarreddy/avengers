from django.test import TestCase
from .models import Fundamentals, Symbols
import logging
from datetime import datetime


class FundmentalsUnitTests (TestCase):
    """Add simple access test for model (Fundamnetals) in thanos app"""

    def setUp(self):
        logging.basicConfig(level=logging.INFO)

    def test_add_entry(self):
        symbol = Symbols()
        symbol.symbol_name = "NOCIL"
        logging.info("Symbol is ( %s )", symbol.symbol_name)
        symbol.market_name = Symbols.MARKETS[0][0]
        logging.info("Symbol Belongs to ( %s )", symbol.market_name)
        symbol.save()
        fundamentals = Fundamentals()
        fundamentals.symbol = symbol
        fundamentals.year = datetime.strptime("2017 01 01", "%Y %m %d")
        logging.info("The year field is set to ( %s )", fundamentals.year)
        fundamentals.save()
        self.assertEqual(1, Fundamentals.objects.all().count())

