from django.test import TestCase
from thanos.models import *
from .views import FundamentalsExtractor
import logging


class MawViewTests(TestCase):

    def setUp(self):
        pass

    def test_extract_ratios(self):
        fundamental_extractor = FundamentalsExtractor(url="file:///home/anup/Downloads/main_page.html", silent=False)
        fundamental_extractor.prepare_soup()
        fundamental_extractor.extract_sector_information()
        fundamental_extractor.extract_symbol_information()
        logging.info("Ratios extracted are ...")
        fundamental_extractor.extract_ratios()
        self.assertEqual(7.42, float(fundamental_extractor.ratios['Basic EPS (Rs.)']['2017']),
                         "Ratios mismatch Expected : ( {} ), Actual : ( {} )".format(7.42, fundamental_extractor.ratios['Basic EPS (Rs.)']['2017']))


    def test_extract_balance_sheet(self):
        fundamental_extractor = FundamentalsExtractor(url="file:///home/anup/Downloads/main_page.html", silent=False)
        fundamental_extractor.prepare_soup()
        fundamental_extractor.extract_sector_information()
        fundamental_extractor.extract_symbol_information()
        logging.info("Balance sheet numbers extracted are ...")
        fundamental_extractor.extract_balance_sheet()
        self.assertEqual(163.58 	, float(fundamental_extractor.balance_sheet['Equity Share Capital']['2017']),
                         "Balance Sheet mismatch, Expected : ( {} ), Actual : ( {} )".format(163.58,
                          fundamental_extractor.balance_sheet['Equity Share Capital']['2017']))

    def test_extract_profit_and_loss(self):
        fundamental_extractor = FundamentalsExtractor(url="file:///home/anup/Downloads/main_page.html", silent=False)
        fundamental_extractor.prepare_soup()
        fundamental_extractor.extract_sector_information()
        fundamental_extractor.extract_symbol_information()
        logging.info("Profit and Loss Statement numbers extracted are ...")
        fundamental_extractor.extract_profit_and_loss_statement()
        self.assertEqual(751.33, float(fundamental_extractor.profit_loss_statement['Total Revenue']['2017']),
                         "Profit and Loss  mismatch, Expected : ( {} ), Actual : ( {} )".format(751.33,
                          fundamental_extractor.profit_loss_statement['Total Revenue']['2017']))

    def test_extract_cash_flow_statement(self):
        fundamental_extractor = FundamentalsExtractor(url="file:///home/anup/Downloads/main_page.html", silent=False)
        fundamental_extractor.prepare_soup()
        fundamental_extractor.extract_sector_information()
        fundamental_extractor.extract_symbol_information()
        logging.info("Cash Flow Statement numbers extracted are ...")
        fundamental_extractor.extract_cash_flow_statement()
        self.assertEqual(140.64, float(fundamental_extractor.cash_flow_statement['Net CashFlow From Operating Activities']['2017']),
                         "Cash Flow statement mismatch, Expected : ( {} ), Actual : ( {} )".format(140.64,
                          fundamental_extractor.cash_flow_statement['Net CashFlow From Operating Activities']['2017']))

    def test_extract_fundamentals(self):
        fundamental_extractor = FundamentalsExtractor(url="file:///home/anup/Downloads/main_page.html", silent=False)
        logging.info("Fundamentals extracting ...")
        fundamental_extractor.extract_fundamentals()
        self.assertEqual(140.64, float(fundamental_extractor.cash_flow_statement['Net CashFlow From Operating Activities']['2017']),
                         "Cash Flow statement mismatch, Expected : ( {} ), Actual : ( {} )".format(140.64,
                          fundamental_extractor.cash_flow_statement['Net CashFlow From Operating Activities']['2017']))
