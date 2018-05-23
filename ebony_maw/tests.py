from django.test import TestCase
from thanos.models import *
from .views import FundamentalsExtractor
import logging


class MawViewTests(TestCase):

    def setUp(self):
        pass

    def test_extract_ratios(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/main_page.html"
        funda.prepare_soup()
        logging.info("Ratios extracted are ...")
        funda.extract_ratios()
        self.assertEqual(7.42, float(funda.ratios['Basic EPS (Rs.)']['2017']),
                         "Ratios mismatch Expected : ( {} ), Actual : ( {} )".format(7.42, funda.ratios['Basic EPS (Rs.)']['2017']))

    def test_push_to_database(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/main_page.html"
        funda.prepare_soup()
        logging.info("Ratios extracted are ...")
        funda.extract_fundamentals()
        funda.push_to_database()
        self.assertEqual(1, Symbol.objects.all().count(),
                         "Database mismatch, Expected : ( {} ), Actual : ( {} )".format(1, Symbol.objects.all().count()))
        self.assertEqual(1, Sector.objects.all().count(),
                         "Database mismatch, Expected : ( {} ), Actual : ( {} )".format(1, Sector.objects.all().count()))
        self.assertEqual(5, Fundamental.objects.all().count(),
                         "Database mismatch, Expected : ( {} ), Actual : ( {} )".format(5, Fundamental.objects.all().count()))
        self.assertEqual(5, BalanceSheet.objects.all().count(),
                         "Database mismatch, Expected : ( {} ), Actual : ( {} )".format(5, BalanceSheet.objects.all().count()))
        self.assertEqual(5, ProfitAndLossStatement.objects.all().count(),
                         "Database mismatch, Expected : ( {} ), Actual : ( {} )".format(5, ProfitAndLossStatement.objects.all().count()))
        self.assertEqual(5, CashFlowStatement.objects.all().count(),
                         "Database mismatch, Expected : ( {} ), Actual : ( {} )".format(5, CashFlowStatement.objects.all().count()))

    def test_extract_balance_sheet(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/main_page.html"
        funda.prepare_soup()
        logging.info("Balance sheet numbers extracted are ...")
        funda.extract_balance_sheet()
        self.assertEqual(163.58 	, float(funda.balance_sheet['Equity Share Capital']['2017']),
                         "Balance Sheet mismatch, Expected : ( {} ), Actual : ( {} )".format(163.58,
                          funda.balance_sheet['Equity Share Capital']['2017']))

    def test_extract_profit_and_loss(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/main_page.html"
        funda.prepare_soup()
        logging.info("Profit and Loss Statement numbers extracted are ...")
        funda.extract_profit_and_loss_statement()
        self.assertEqual(751.33, float(funda.profit_loss_statement['Total Revenue']['2017']),
                         "Profit and Loss  mismatch, Expected : ( {} ), Actual : ( {} )".format(751.33,
                          funda.profit_loss_statement['Total Revenue']['2017']))

    def test_extract_cash_flow_statement(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/main_page.html"
        funda.prepare_soup()
        logging.info("Cash Flow Statement numbers extracted are ...")
        funda.extract_cash_flow_statement()
        self.assertEqual(140.64, float(funda.cash_flow_statement['Net CashFlow From Operating Activities']['2017']),
                         "Cash Flow statement mismatch, Expected : ( {} ), Actual : ( {} )".format(140.64,
                          funda.cash_flow_statement['Net CashFlow From Operating Activities']['2017']))

    def test_extract_fundamentals(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/main_page.html"
        logging.info("Fundamentals extracting ...")
        funda.extract_fundamentals()
        self.assertEqual(140.64, float(funda.cash_flow_statement['Net CashFlow From Operating Activities']['2017']),
                         "Cash Flow statement mismatch, Expected : ( {} ), Actual : ( {} )".format(140.64,
                          funda.cash_flow_statement['Net CashFlow From Operating Activities']['2017']))

    def test_extract_sector(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/main_page.html"
        logging.info("Extracting Sectorial information ...")
        funda.extract_sector_information()
        self.assertEqual("Petrochemicals", funda.sector, "Sector mismatch, Expected: ( {} ), Actual: ( {} )".
                         format("Petrochemicals", funda.sector))

    def test_extract_symbol(self):
        funda = FundamentalsExtractor(silent=False)
        funda.url = "file:///home/anup/Downloads/main_page.html"
        logging.info("Extracting Symbol information ...")
        funda.extract_symbol_information()
        self.assertEqual("NOCIL", funda.symbol_name, "Symbol mismatch, Expected: ( {} ), Actual: ( {} )".
                         format("NOCIL", funda.symbol_name))
