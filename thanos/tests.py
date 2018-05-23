from django.test import TestCase
from .models import Fundamental, Symbol, BalanceSheet, ProfitAndLossStatement, CashFlowStatement
import logging
from datetime import datetime


class ThanosModelTests (TestCase):
    """Add simple access test for model (Fundamentals) in thanos app"""

    def setUp(self):
        logging.basicConfig(level=logging.INFO)

    def test_add_entry(self):
        symbol = Symbol()
        symbol.symbol_name = "NOCIL"
        logging.info("Symbol is ( %s )", symbol.symbol_name)
        symbol.market_name = Symbol.MARKETS[0][0]
        logging.info("Symbol Belongs to ( %s )", symbol.market_name)
        symbol.save()
        fundamentals = Fundamental()
        fundamentals.symbol = symbol
        fundamentals.year = datetime.strptime("2017 01 01", "%Y %m %d")
        logging.info("The year field is set to ( %s )", fundamentals.year)
        fundamentals.save()
        self.assertEqual(1, Fundamental.objects.all().count())

    def test_balance_sheet_model(self):
        symbol = Symbol()
        symbol.symbol_name = "NOCIL"
        logging.info("Symbol is ( %s )", symbol.symbol_name)
        symbol.market_name = Symbol.MARKETS[0][0]
        logging.info("Symbol Belongs to ( %s )", symbol.market_name)
        symbol.save()
        balance_sheet = BalanceSheet()
        balance_sheet.symbol = symbol
        balance_sheet.year = datetime.strptime("2017 01 01", "%Y %m %d")
        logging.info("The year field is set to ( %s )", balance_sheet.year)
        balance_sheet.save()
        self.assertEqual(1, BalanceSheet.objects.all().count())

    def test_profit_and_loss_model(self):
        symbol = Symbol()
        symbol.symbol_name = "NOCIL"
        logging.info("Symbol is ( %s )", symbol.symbol_name)
        symbol.market_name = Symbol.MARKETS[0][0]
        logging.info("Symbol Belongs to ( %s )", symbol.market_name)
        symbol.save()
        profit_and_loss_sheet = ProfitAndLossStatement()
        profit_and_loss_sheet.symbol = symbol
        profit_and_loss_sheet.year = datetime.strptime("2017 01 01", "%Y %m %d")
        logging.info("The year field is set to ( %s )", profit_and_loss_sheet.year)
        profit_and_loss_sheet.save()
        self.assertEqual(1, ProfitAndLossStatement.objects.all().count())

    def test_cash_flow_sheet_model(self):
        symbol = Symbol()
        symbol.symbol_name = "NOCIL"
        logging.info("Symbol is ( %s )", symbol.symbol_name)
        symbol.market_name = Symbol.MARKETS[0][0]
        logging.info("Symbol Belongs to ( %s )", symbol.market_name)
        symbol.save()
        cash_flow_sheet = CashFlowStatement()
        cash_flow_sheet.symbol = symbol
        cash_flow_sheet.year = datetime.strptime("2017 01 01", "%Y %m %d")
        logging.info("The year field is set to ( %s )", cash_flow_sheet.year)
        cash_flow_sheet.save()
        self.assertEqual(1, CashFlowStatement.objects.all().count())




