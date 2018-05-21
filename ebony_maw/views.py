from django.http import HttpResponse
from thanos.models import Fundamentals, Symbols, ProfitAndLossStatement, CashFlowStatement, BalanceSheet
from django.template import loader
from django.views.generic import TemplateView
from bs4 import BeautifulSoup as soup
import logging
import urllib
from datetime import datetime


class MawMainPage (TemplateView):
    template_name = 'maw/maw.html'

    def post(self, request, *args, **kwargs):
        url = request.POST['url']
        fundamentals = FundamentalsExtractor(url, silent=False)
        fundamentals.extract_fundamentals()
        fundamentals.push_to_database()
        data = "Extraction done..."
        maw = loader.get_template(self.template_name)
        return HttpResponse(maw.render({'url': data}, request))


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
    ratios = {}
    balance_sheet = {}
    profit_loss_statement = {}
    cash_flow_statement = {}
    log_stream = ""
    symbol_name = ""

    def __init__(self, url="", silent=True):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        logger.disabled = silent
        if url == "":
            logging.warning("URL is not set properly")
        else:
            self.url = url
            logging.info("URL is set as %s ", url)

    def __valiidate_url(self):
        pass

    def __prepare_soup(self):
        if self.__is_url_present():
            self.my_soup = soup(urllib.urlopen(self.url), "html.parser")
        else:
            logging.error("Cannot process fundamentals as URL is not set")

    def __is_url_present(self):
        return self.url != ""

    def extract_fundamentals(self):
        self.__prepare_soup()
        self.extract_ratios()

    def extract_balance_sheet(self):
        self.__prepare_soup()
        table = self.my_soup.find_all('table', {'class': 'table4'})[2]
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

    def extract_profit_and_loss_statement(self):
        self.__prepare_soup()
        table = self.my_soup.find_all('table', {'class': 'table4'})[2]
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

    def extract_cash_flow_statement(self):
        self.__prepare_soup()
        table = self.my_soup.find_all('table', {'class': 'table4'})[2]
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

    def extract_ratios(self):
        self.symbol_name = self.my_soup.find('h1', {'class': 'b_42 PT20'}).get_text()
        logging.info("  Extracting Symbol ( %s ) ...", self.symbol_name)
        table = self.my_soup.find_all('table', {'class': 'table4'})[2]
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

    def push_to_database(self):
        years_list = ['2017', '2016', '2015', '2014', '2013']
        symbol_name = self.symbol_name
        symbol = Symbols()
        symbol.symbol_name = symbol_name
        symbol.market_name = Symbols.MARKETS[0][0]
        symbol.save()
        for i in range(5):
            fundamentals = Fundamentals()
            fundamentals.symbol = symbol
            fundamentals.year = datetime.strptime(years_list[i]+' 01 01', '%Y %m %d')
            for field, name in self.RATIOS_NAMES:
                if name in self.ratios:
                    setattr(fundamentals, field, self.ratios[name][years_list[i]])
            fundamentals.save()
            balance_sheet = BalanceSheet()
            balance_sheet.symbol = symbol
            balance_sheet.sheet_year = datetime.strptime(years_list[i]+' 01 01', '%Y %m %d')
            for field, name in self.BALANCE_SHEET_NAMES:
                if name in self.ratios:
                    setattr(balance_sheet, field, self.ratios[name][years_list[i]])
            balance_sheet.save()
            profit_loss_statement = ProfitAndLossStatement()
            profit_loss_statement.symbol = symbol
            profit_loss_statement.sheet_year = datetime.strptime(years_list[i] + ' 01 01', '%Y %m %d')
            for field, name in self.PROFIT_AND_LOSS_STATEMENT_NAMES:
                if name in self.ratios:
                    setattr(profit_loss_statement, field, self.ratios[name][years_list[i]])
            profit_loss_statement.save()
            cash_flow_statement = CashFlowStatement()
            cash_flow_statement.symbol = symbol
            cash_flow_statement.sheet_year = datetime.strptime(years_list[i] + ' 01 01', '%Y %m %d')
            for field, name in self.CASH_FLOW_STATEMENT_NAMES:
                if name in self.ratios:
                    setattr(cash_flow_statement, field, self.ratios[name][years_list[i]])
            cash_flow_statement.save()
