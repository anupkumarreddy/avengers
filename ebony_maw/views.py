from django.http import HttpResponse
from thanos.models import *
from django.template import loader
from django.views.generic import TemplateView
from bs4 import BeautifulSoup as soup
import logging
import urllib
from datetime import datetime
import re


class MawMainPage (TemplateView):
    template_name = 'maw/dashboard.html'

    def get(self, request, symbol_id=0):
        return self.serve(request, symbol_id)

    def post(self, request, symbol_id=0):
        url = request.POST['url']
        fundamentals = FundamentalsExtractor(url, silent=False)
        new_symbol_id = fundamentals.extract_fundamentals()
        return self.serve(request, new_symbol_id)

    def serve(self, request, symbol_id = 0):
        data = {}
        all_symbols = Symbol.objects.all()
        requested_symbol = Symbol.objects.filter(pk=symbol_id)
        if len(requested_symbol):
            requested_symbol = Symbol.objects.get(pk=symbol_id)
        else:
            requested_symbol = all_symbols[0]
        balance_sheet = BalanceSheet.objects.get(symbol_id=requested_symbol, sheet_year__year=2017)
        data['requested_symbol'] = requested_symbol
        company = {'liabilities': int(((balance_sheet.total_non_current_liabilities + balance_sheet.total_current_libilities) / balance_sheet.total_assets) * 100),
                   'assets': balance_sheet.total_assets,
                   'equity': int((balance_sheet.total_share_holders_fund / balance_sheet.total_assets) * 100)}
        profit_loss_statement = ProfitAndLossStatement.objects.get(symbol_id=requested_symbol, sheet_year__year=2017)
        pl = {'revenue': profit_loss_statement.total_revenue, 'expences': profit_loss_statement.total_expenses,
              'profit': profit_loss_statement.profit_loss_for_the_period,
              'tax': (profit_loss_statement.total_revenue-(profit_loss_statement.total_expenses + profit_loss_statement.profit_loss_for_the_period))}
        cash_flow_statement = CashFlowStatement.objects.get(symbol_id=requested_symbol, sheet_year__year=2017)
        cf = {'operating_activities': cash_flow_statement.net_cash_flow_from_operating_activities,
              'investing_activities': cash_flow_statement.net_cash_used_in_investing_activities,
              'financing_activities': cash_flow_statement.net_cash_used_from_financing_activities,
              'others': cash_flow_statement.net_inc_dec_cash_and_cash_equivalents -
                        (cash_flow_statement.net_cash_flow_from_operating_activities+
                         cash_flow_statement.net_cash_used_in_investing_activities+
                         cash_flow_statement.net_cash_used_from_financing_activities)
              }
        balance_history = BalanceSheet.objects.filter(symbol_id=requested_symbol).order_by('sheet_year')
        data['company'] = company
        data['all_symbols'] = all_symbols
        data['pl'] = pl
        data['cf'] = cf
        data['balance_hist'] = balance_history
        maw = loader.get_template(self.template_name)
        return HttpResponse(maw.render({'data': data}, request))


class FundamentalsExtractor:
    """Extracts all fundamental data for a single quote from money control web pages"""

    RATIOS_NAMES = (
        ('basic_eps_rs', 'Basic EPS (Rs.)'),
        ('diluted_eps_rs', 'Diluted EPS (Rs.)'),
        ('cash_eps_in_rs', 'Cash EPS (Rs.)'),
        ('book_value_exc_reserve_rs', 'Book Value [ExclRevalReserve]/Share (Rs.)'),
        ('book_value_inc_reserve_rs', 'Book Value [InclRevalReserve]/Share (Rs.)'),
        ('dividend_rs', 'Dividend / Share(Rs.)'),
        ('revenue_from_operations_rs', 'Revenue from Operations/Share (Rs.)'),
        ('pbdit_rs', 'PBDIT/Share (Rs.)'),
        ('pbit_rs', 'PBIT/Share (Rs.)'),
        ('pbt_rs', 'PBT/Share (Rs.)'),
        ('net_profit_rs', 'Net Profit/Share (Rs.)'),
        ('pbdit_margin_percent', 'PBDIT Margin (%)'),
        ('pbit_margin_percent', 'PBIT Margin (%)'),
        ('pbt_margin_percent', 'PBT Margin (%)'),
        ('net_profit_margin_percent', 'Net Profit Margin (%)'),
        ('return_on_networth_percent', 'Return on Networth / Equity (%)'),
        ('return_on_capital_employed_percent', 'Return on Capital Employed (%)'),
        ('return_on_assets_percent', 'Return on Assets (%)'),
        ('total_dept_to_equity_x', 'Total Debt/Equity (X)'),
        ('asset_turnover_ratio_percent', 'Asset Turnover Ratio (%)'),
        ('current_ratio_x', 'Current Ratio (X)'),
        ('quick_ratio_x', 'Quick Ratio (X)'),
        ('inventory_turnover_ratio_x', 'Inventory Turnover Ratio (X)'),
        ('dividend_payout_ratio_cp_percent', 'Dividend  Payout Ratio (NP) (%)'),
        ('dividend_payout_ratio_np_percent', 'Dividend Payout Ratio (CP) (%)'),
        ('earnings_retention_ratio_percent', 'Earnings Retention Ratio (%)'),
        ('cach_earnings_retention_ratio_percent', 'Cash Earnings Retention Ratio (%)'),
        ('enterprice_value_cr', 'Enterprise Value (Cr.)'),
        ('ev_over_net_operating_revenue_x', 'EV/Net Operating Revenue (X)'),
        ('ev_over_ebitda_x', 'EV/EBITDA (X)'),
        ('marketcap_over_net_operating_revenue_x', 'MarketCap/Net Operating Revenue (X)'),
        ('retention_ratios_percent', 'Retention Ratios (%)'),
        ('price_over_book_x', 'Price/BV (X)'),
        ('price_over_net_operating_revenue_x', 'Price/Net Operating Revenue'),
        ('earnings_yield', 'Earnings Yield')
    )

    BALANCE_SHEET_NAMES = (
        ('equity_share_capital', 'Equity Share Capital'),
        ('reserves_and_surples', 'Reserves and Surplus'),
        ('total_share_holders_fund', 'Total Shareholders Funds'),
        ('long_term_borrowings', 'Long Term Borrowings'),
        ('deferred_tax_liabilities_net', 'Deferred Tax Liabilities [Net]'),
        ('long_term_provisions', 'Long Term Provisions'),
        ('total_non_current_liabilities', 'Total Non-Current Liabilities'),
        ('short_term_borrowings', 'Short Term Borrowings'),
        ('trade_payables', 'Trade Payables'),
        ('other_current_liabilities', 'Other Current Liabilities'),
        ('short_term_provisions', 'Short Term Provisions'),
        ('total_current_libilities', 'Total Current Liabilities'),
        ('total_capital_and_liabilities', 'Total Capital And Liabilities'),
        ('tangible_assets', 'Tangible Assets'),
        ('intangible_assets', 'Intangible Assets'),
        ('capital_work_in_progress', 'Capital Work-In-Progress'),
        ('fixed_assets', 'Fixed Assets'),
        ('non_current_investments', 'Non-Current Investments'),
        ('long_term_loans_and_advances', 'Long Term Loans And Advances'),
        ('total_non_current_assets', 'Total Non-Current Assets'),
        ('inventories', 'Inventories'),
        ('trade_receivables', 'Trade Receivables'),
        ('cash_and_cach_equivalents', 'Cash And Cash Equivalents'),
        ('short_term_loans_and_advances', 'Short Term Loans And Advances'),
        ('other_current_assets', 'OtherCurrentAssets'),
        ('total_current_assets', 'Total Current Assets'),
        ('total_assets', 'Total Assets')
    )

    PROFIT_AND_LOSS_STATEMENT_NAMES = (
        ('revenue_from_operation_gross', 'Revenue From Operations [Gross]'),
        ('excise_service_tax',  'Less: Excise/Sevice Tax/Other Levies'),
        ('revenue_from_operations', 'Revenue From Operations [Net]'),
        ('other_operating_revenue', 'Other Operating Revenues'),
        ('total_operating_revenue', 'Total Operating Revenues'),
        ('other_income',  'Other Income'),
        ('total_revenue',  'Total Revenue'),
        ('cost_of_materials_consumed', 'Cost Of Materials Consumed'),
        ('purchase_of_stock_in_trade', 'Purchase Of Stock-In Trade'),
        ('changes_in_inventories', 'Changes In Inventories Of FG,WIP And Stock-In Trade'),
        ('employee_benefit_expenses', 'Employee Benefit Expenses'),
        ('finance_cost', 'Finance Costs'),
        ('depreciation_and_amortisation_expenses', 'Depreciation And Amortisation Expenses'),
        ('other_expenses', 'Other Expenses'),
        ('total_expenses', 'Total Expenses'),
        ('profit_loss_before_extraordinary_items', 'Profit/Loss Before Exceptional, ExtraOrdinary Items And Tax'),
        ('exceptional_items', 'Exceptional Items'),
        ('profit_loss_before_tax', 'Profit/Loss Before Tax'),
        ('current_tax', 'Current Tax'),
        ('deferred_tax', 'Deferred Tax'),
        ('tax_for_earliar_years', 'Tax For Earlier Years'),
        ('total_tax_expense', 'Total Tax Expenses'),
        ('profit_loss_after_tax_before_extraordinary_items', 'Profit/Loss After Tax And Before ExtraOrdinary Items'),
        ('profit_loss_from_continuing_operations', 'Profit/Loss From Continuing Operations'),
        ('profit_loss_for_the_period', 'Profit/Loss For The Period')
    )

    CASH_FLOW_STATEMENT_NAMES = (
        ('net_profit_loss_before_extraordinary_and_tax', 'Net Profit/Loss Before Extraordinary Items And Tax'),
        ('net_cash_flow_from_operating_activities', 'Net CashFlow From Operating Activities'),
        ('net_cash_used_in_investing_activities', 'Net Cash Used In Investing Activities'),
        ('net_cash_used_from_financing_activities', 'Net Cash Used From Financing Activities'),
        ('foreign_exchange_gains_losses', 'Foreign Exchange Gains / Losses'),
        ('net_inc_dec_cash_and_cash_equivalents', 'Net Inc/Dec In Cash And Cash Equivalents'),
        ('cash_and_cash_equivalents_begin_of_year', 'Cash And Cash Equivalents Begin of Year'),
        ('cash_and_cash_equivalents_end_of_year', 'Cash And Cash Equivalents End Of Year'),
    )

    url = ""
    symbol_id = -1
    ratios = {}
    balance_sheet = {}
    profit_loss_statement = {}
    cash_flow_statement = {}
    symbol_name = ""
    sector = ""
    base_url = "http://www.moneycontrol.com"
    balance_sheet_url = ""
    profit_loss_url = ""
    cash_flow_url = ""
    ratios_url = ""
    years_list = ['2017', '2016', '2015', '2014', '2013']
    extraction_status = {'URL': False, 'SUB_URLS': False, 'SYMBOL': False, 'SECTOR': False, 'BALANCE_SHEET': False,
                         'PROFIT_LOSS_STATEMENT': False, 'CASH_FLOW_STATEMENT': False, 'RATIOS': False}

    def __init__(self, url="", silent=True):
        """constructor for extractor, assumes url must be present"""
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        logger.disabled = silent
        if url == "":
            logging.warning("URL is not set properly")
        else:
            self.url = url
            self.extraction_status['URL'] = True
            logging.info("URL is set as %s ", url)

    def __extraction_is_clean(self):
        status = True
        for item in self.extraction_status.values():
            if not item:
                status = False
        return status

    def __already_done(self, flow):
        return self.extraction_status[flow]

    def __symbol_is_new(self):
        status = True
        symbol = Symbol.objects.filter(symbol_name__exact=self.symbol_name)
        if symbol:
            status = False
        return status

    def __save_sector(self):
        sector = Sector.objects.filter(sector_name__exact=self.sector)
        if not sector:
            sector = Sector()
            sector.sector_name = self.sector
            sector.save()

    def __save_symbol(self):
        symbol = Symbol()
        symbol.symbol_name = self.symbol_name
        symbol.market_name = Symbol.MARKETS[0][0]
        symbol.symbol_sector_name = Sector.objects.get(sector_name__exact=self.sector)
        symbol.symbol_url = self.url
        symbol.save()
        self.symbol_id = symbol.id

    def __save_balance_sheet(self):
        for i in range(len(self.years_list)):
            balance_sheet = BalanceSheet()
            balance_sheet.symbol = Symbol.objects.get(symbol_name__exact=self.symbol_name)
            balance_sheet.sheet_year = datetime.strptime(self.years_list[i] + ' 01 01', '%Y %m %d')
            for field, name in self.BALANCE_SHEET_NAMES:
                if name in self.balance_sheet:
                    setattr(balance_sheet, field, self.balance_sheet[name][self.years_list[i]])
            balance_sheet.save()

    def __save_profit_loss_statement(self):
        for i in range(len(self.years_list)):
            profit_loss_statement = ProfitAndLossStatement()
            profit_loss_statement.symbol = Symbol.objects.get(symbol_name__exact=self.symbol_name)
            profit_loss_statement.sheet_year = datetime.strptime(self.years_list[i] + ' 01 01', '%Y %m %d')
            for field, name in self.PROFIT_AND_LOSS_STATEMENT_NAMES:
                if name in self.profit_loss_statement:
                    setattr(profit_loss_statement, field, self.profit_loss_statement[name][self.years_list[i]])
            profit_loss_statement.save()

    def __save_cash_flow_statement(self):
        for i in range(len(self.years_list)):
            cash_flow_statement = CashFlowStatement()
            cash_flow_statement.symbol = Symbol.objects.get(symbol_name__exact=self.symbol_name)
            cash_flow_statement.sheet_year = datetime.strptime(self.years_list[i] + ' 01 01', '%Y %m %d')
            for field, name in self.CASH_FLOW_STATEMENT_NAMES:
                if name in self.cash_flow_statement:
                    setattr(cash_flow_statement, field, self.cash_flow_statement[name][self.years_list[i]])
            cash_flow_statement.save()

    def __save_ratios(self):
        for i in range(len(self.years_list)):
            fundamentals = Fundamental()
            fundamentals.symbol = Symbol.objects.get(symbol_name__exact=self.symbol_name)
            fundamentals.year = datetime.strptime(self.years_list[i] + ' 01 01', '%Y %m %d')
            for field, name in self.RATIOS_NAMES:
                if name in self.ratios:
                    setattr(fundamentals, field, self.ratios[name][self.years_list[i]])
            fundamentals.save()

    def prepare_soup(self):
        """Extracts all financial links from the main page"""
        if self.__already_done('URL'):
            my_soup = soup(urllib.urlopen(self.url), "html.parser")
            financial_links = my_soup.find_all('a', {'href': re.compile(r'/financials/.*')})
            self.balance_sheet_url = self.base_url + financial_links[1]['href']
            self.profit_loss_url = self.base_url + financial_links[2]['href']
            self.cash_flow_url = self.base_url + financial_links[7]['href']
            self.ratios_url = self.base_url + financial_links[8]['href']
            logging.info("  Link:%s", self.balance_sheet_url)
            if self.balance_sheet_url and self.profit_loss_url and self.cash_flow_url and self.ratios_url:
                self.extraction_status['SUB_URLS'] = True

    def extract_sector_information(self):
        """Extracts sector related information"""
        if self.__already_done('URL'):
            my_soup = soup(urllib.urlopen(self.url), "html.parser")
            self.sector = my_soup.find('a', {'href': re.compile(r'.*/stocks/sectors/.*')}).get_text()
            if self.sector:
                logging.info("   Extracting Sector name ( %s )", self.sector)
                self.extraction_status['SECTOR'] = True

    def extract_symbol_information(self):
        """Extracts symbol related information"""
        if self.__already_done('URL') and self.__already_done('SECTOR'):
            my_soup = soup(urllib.urlopen(self.url), "html.parser")
            div = my_soup.find('div', {'class': 'FL gry10'})
            if div:
                match = re.match('.* NSE: (\w+) |.*', div.get_text())
                if match:
                    logging.info(match.group(1))
                    self.symbol_name = match.group(1)
                    logging.info("   Extracting Symbol name ( %s )", self.symbol_name)
                    self.extraction_status['SYMBOL'] = True
                else:
                    logging.error("   Symbol not Found ...")

    def extract_balance_sheet(self):
        """Extracts balance sheet from financial url"""
        if self.__already_done('SUB_URLS') and self.__already_done('SYMBOL'):
            my_soup = soup(urllib.urlopen(self.balance_sheet_url), "html.parser")
            table = my_soup.find_all('table', {'class': 'table4'})[2]
            if table:
                for index, tr in enumerate(table.find_all('tr')):
                    td = tr.find_all('td')
                    if len(td) == 6 and td[0].get_text() != "" and td[1].get_text() != "" \
                            and td[2].get_text() != "" and td[3].get_text() != "" \
                            and td[4].get_text() != "" and td[5].get_text() != "":
                        logging.info("  Extracting %s: (%s, %s, %s, %s, %s) ... ", td[0].get_text(),
                                     td[1].get_text(),
                                     td[2].get_text(),
                                     td[3].get_text(),
                                     td[4].get_text(),
                                     td[5].get_text())
                        self.balance_sheet[td[0].get_text()] = {'2017': td[1].get_text().replace(',', ''),
                                                                '2016': td[2].get_text().replace(',', ''),
                                                                '2015': td[3].get_text().replace(',', ''),
                                                                '2014': td[4].get_text().replace(',', ''),
                                                                '2013': td[5].get_text().replace(',', '')}
                self.extraction_status['BALANCE_SHEET'] = True

    def extract_profit_and_loss_statement(self):
        """Extracts profit and loss statement from finacial url"""
        if self.__already_done('SUB_URLS') and self.__already_done('SYMBOL'):
            my_soup = soup(urllib.urlopen(self.profit_loss_url), "html.parser")
            table = my_soup.find_all('table', {'class': 'table4'})[2]
            if table:
                for index, tr in enumerate(table.find_all('tr')):
                    td = tr.find_all('td')
                    if len(td) == 6 and td[0].get_text() != "" and td[1].get_text() != "" \
                            and td[2].get_text() != "" and td[3].get_text() != "" \
                            and td[4].get_text() != "" and td[5].get_text() != "":
                        logging.info("  Extracting %s: (%s, %s, %s, %s, %s) ... ", td[0].get_text(),
                                     td[1].get_text(),
                                     td[2].get_text(),
                                     td[3].get_text(),
                                     td[4].get_text(),
                                     td[5].get_text())
                        self.profit_loss_statement[td[0].get_text()] = {'2017': td[1].get_text().replace(',', ''),
                                                                        '2016': td[2].get_text().replace(',', ''),
                                                                        '2015': td[3].get_text().replace(',', ''),
                                                                        '2014': td[4].get_text().replace(',', ''),
                                                                        '2013': td[5].get_text().replace(',', '')}
                self.extraction_status['PROFIT_LOSS_STATEMENT'] = True

    def extract_cash_flow_statement(self):
        """Extracts cash flow statement from financial url"""
        if self.__already_done('SUB_URLS') and self.__already_done('SYMBOL'):
            my_soup = soup(urllib.urlopen(self.cash_flow_url), "html.parser")
            table = my_soup.find_all('table', {'class': 'table4'})[2]
            if table:
                for index, tr in enumerate(table.find_all('tr')):
                    td = tr.find_all('td')
                    if len(td) == 6 and td[0].get_text() != "" and td[1].get_text() != "" \
                            and td[2].get_text() != "" and td[3].get_text() != "" \
                            and td[4].get_text() != "" and td[5].get_text() != "":
                        logging.info("  Extracting %s: (%s, %s, %s, %s, %s) ... ", td[0].get_text(),
                                     td[1].get_text(),
                                     td[2].get_text(),
                                     td[3].get_text(),
                                     td[4].get_text(),
                                     td[5].get_text())
                        self.cash_flow_statement[td[0].get_text()] = {'2017': td[1].get_text().replace(',', ''),
                                                                      '2016': td[2].get_text().replace(',', ''),
                                                                      '2015': td[3].get_text().replace(',', ''),
                                                                      '2014': td[4].get_text().replace(',', ''),
                                                                      '2013': td[5].get_text().replace(',', '')}
                self.extraction_status['CASH_FLOW_STATEMENT'] = True

    def extract_ratios(self):
        """Extracts ratios information from financial url"""
        if self.__already_done('SUB_URLS') and self.__already_done('SYMBOL'):
            my_soup = soup(urllib.urlopen(self.ratios_url), "html.parser")
            logging.info("  Extracting Symbol ( %s ) ...", self.symbol_name)
            table = my_soup.find_all('table', {'class': 'table4'})[2]
            if table:
                for index, tr in enumerate(table.find_all('tr')):
                    td = tr.find_all('td')
                    if len(td) == 6 and td[0].get_text() != "" and td[1].get_text() != "" \
                            and td[2].get_text() != "" and td[3].get_text() != "" \
                            and td[4].get_text() != "" and td[5].get_text() != "":
                        logging.info("  Extracting %s: (%s, %s, %s, %s, %s) ... ", td[0].get_text(),
                                     td[1].get_text(),
                                     td[2].get_text(),
                                     td[3].get_text(),
                                     td[4].get_text(),
                                     td[5].get_text())
                        self.ratios[td[0].get_text()] = {'2017': td[1].get_text().replace(',', ''),
                                                         '2016': td[2].get_text().replace(',', ''),
                                                         '2015': td[3].get_text().replace(',', ''),
                                                         '2014': td[4].get_text().replace(',', ''),
                                                         '2013': td[5].get_text().replace(',', '')}
                self.extraction_status['RATIOS'] = True

    def push_to_database(self):
        """Store all information to the database"""
        if self.__extraction_is_clean() and self.__symbol_is_new():
            self.__save_sector()
            self.__save_symbol()
            self.__save_balance_sheet()
            self.__save_profit_loss_statement()
            self.__save_cash_flow_statement()
            self.__save_ratios()

    def extract_fundamentals(self):
        for phase in self.phases:
            phase(self)
        return self.symbol_id

    phases = [prepare_soup, extract_sector_information, extract_symbol_information, extract_balance_sheet,
              extract_profit_and_loss_statement, extract_cash_flow_statement, extract_ratios, push_to_database]

