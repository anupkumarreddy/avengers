from django.test import TestCase
from thanos.models import Fundamentals, Symbols
from .views import FundamentalsExtractor
import logging


class MawViewTests(TestCase):

    def setUp(self):
        pass

    def test_extract_fundamentals(self):
        funda = FundamentalsExtractor()
        funda.url = "file:///home/anup/Downloads/Nocil.html"
        logging.info("Ratios extracted are ...")
        funda.extract_fundamentals()
        self.assertEqual(7.42, float(funda.ratios['Basic EPS (Rs.)']['2017']),
                         "Ratios mismatch Expected : ( {} ), Actual : ( {} )".format(7.42, funda.ratios['Basic EPS (Rs.)']['2017']))
        self.assertEqual('NOCIL', funda.symbol_name,
                         "Symbol name mismatch, Expected : ( {} ), Actual : ( {} )".format('NOCIL', funda.symbol_name))

    def test_push_to_database(self):
        funda = FundamentalsExtractor()
        funda.url = "file:///home/anup/Downloads/Nocil.html"
        logging.info("Ratios extracted are ...")
        funda.extract_fundamentals()
        funda.push_to_database()
        self.assertEqual(1, Symbols.objects.all().count(),
                         "Database mismatch, Expected : ( {} ), Actual : ( {} )".format(1, Symbols.objects.all().count()))
        self.assertEqual(5, Fundamentals.objects.all().count(),
                         "Database mismatch, Expected : ( {} ), Actual : ( {} )".format(5, Fundamentals.objects.all().count()))

