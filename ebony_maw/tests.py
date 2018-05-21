from django.test import TestCase
from thanos.models import Fundamentals, Symbols
from .views import FundamentalsExtractor
import logging


class MawViewTests(TestCase):

    def setUp(self):
        pass

    def test_extract_ratios(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/Nocil.html"
        logging.info("Ratios extracted are ...")
        funda.extract_fundamentals()
        self.assertEqual(7.42, float(funda.ratios['Basic EPS (Rs.)']['2017']),
                         "Ratios mismatch Expected : ( {} ), Actual : ( {} )".format(7.42, funda.ratios['Basic EPS (Rs.)']['2017']))
        self.assertEqual('NOCIL', funda.symbol_name,
                         "Symbol name mismatch, Expected : ( {} ), Actual : ( {} )".format('NOCIL', funda.symbol_name))

    def test_push_to_database(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/Nocil.html"
        logging.info("Ratios extracted are ...")
        funda.extract_fundamentals()
        funda.push_to_database()
        self.assertEqual(1, Symbols.objects.all().count(),
                         "Database mismatch, Expected : ( {} ), Actual : ( {} )".format(1, Symbols.objects.all().count()))
        self.assertEqual(5, Fundamentals.objects.all().count(),
                         "Database mismatch, Expected : ( {} ), Actual : ( {} )".format(5, Fundamentals.objects.all().count()))

    def test_extract_balance_sheet(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/balance_sheet.html"
        logging.info("Balance sheet numbers extracted are ...")
        funda.extract_balance_sheet()
        self.assertEqual(163.58 	, float(funda.balance_sheet['Equity Share Capital']['2017']),
                         "Balance Sheet mismatch, Expected : ( {} ), Actual : ( {} )".format(163.58,
                          funda.balance_sheet['Equity Share Capital']['2017']))

    def test_extract_profit_and_loss(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/profit_loss.html"
        logging.info("Profit and Loss Statement numbers extracted are ...")
        funda.extract_profit_and_loss_statement()
        self.assertEqual(751.33, float(funda.profit_loss_statement['Total Revenue']['2017']),
                         "Profit and Loss  mismatch, Expected : ( {} ), Actual : ( {} )".format(751.33,
                          funda.profit_loss_statement['Total Revenue']['2017']))

    def test_extract_cash_flow_statement(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/cash_flow.html"
        logging.info("Cash Flow Statement numbers extracted are ...")
        funda.extract_cash_flow_statement()
        self.assertEqual(140.64, float(funda.cash_flow_statement['Net CashFlow From Operating Activities']['2017']),
                         "Cash Flow statement mismatch, Expected : ( {} ), Actual : ( {} )".format(140.64,
                          funda.cash_flow_statement['Net CashFlow From Operating Activities']['2017']))

