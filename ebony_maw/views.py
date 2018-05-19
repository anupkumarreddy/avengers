from django.http import HttpResponse
from thanos.models import Fundamentals, Symbols
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

    url = ""
    ratios = {}
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
        # self.__validate_url()
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
            fundamentals.basic_eps_rs = self.ratios['Basic EPS (Rs.)'][years_list[i]]
            fundamentals.diluted_eps_rs = self.ratios['Diluted EPS (Rs.)'][years_list[i]]
            fundamentals.cash_eps_in_rs = self.ratios['Cash EPS (Rs.)'][years_list[i]]
            fundamentals.book_value_exc_reserve_rs = self.ratios['Book Value [ExclRevalReserve]/Share (Rs.)'][years_list[i]]
            fundamentals.book_value_inc_reserve_rs = self.ratios['Book Value [InclRevalReserve]/Share (Rs.)'][years_list[i]]
            fundamentals.dividend_rs = self.ratios['Dividend / Share(Rs.)'][years_list[i]]
            fundamentals.revenue_from_operations_rs = self.ratios['Revenue from Operations/Share (Rs.)'][years_list[i]]
            fundamentals.pbdit_rs = self.ratios['PBDIT/Share (Rs.)'][years_list[i]]
            fundamentals.pbit_rs = self.ratios['PBIT/Share (Rs.)'][years_list[i]]
            fundamentals.pbt_rs = self.ratios['PBT/Share (Rs.)'][years_list[i]]
            fundamentals.net_profit_rs = self.ratios['Net Profit/Share (Rs.)'][years_list[i]]
            fundamentals.pbdit_margin_percent = self.ratios['PBDIT Margin (%)'][years_list[i]]
            fundamentals.pbit_margin_percent = self.ratios['PBIT Margin (%)'][years_list[i]]
            fundamentals.pbt_margin_percent = self.ratios['PBT Margin (%)'][years_list[i]]
            fundamentals.net_profit_margin_percent = self.ratios['Net Profit Margin (%)'][years_list[i]]
            fundamentals.return_on_networth_percent = self.ratios['Return on Networth / Equity (%)'][years_list[i]]
            fundamentals.return_on_capital_employed_percent = self.ratios['Return on Capital Employed (%)'][years_list[i]]
            fundamentals.return_on_assets_percent = self.ratios['Return on Assets (%)'][years_list[i]]
            fundamentals.total_dept_to_equity_x = self.ratios['Total Debt/Equity (X)'][years_list[i]]
            fundamentals.asset_turnover_ratio_percent = self.ratios['Asset Turnover Ratio (%)'][years_list[i]]
            fundamentals.current_ratio_x = self.ratios['Current Ratio (X)'][years_list[i]]
            fundamentals.quick_ratio_x = self.ratios['Quick Ratio (X)'][years_list[i]]
            fundamentals.inventory_turnover_ratio_x = self.ratios['Inventory Turnover Ratio (X)'][years_list[i]]
            fundamentals.dividend_payout_ratio_cp_percent = self.ratios['Dividend  Payout Ratio (NP) (%)'][years_list[i]]
            fundamentals.dividend_payout_ratio_np_percent = self.ratios['Dividend Payout Ratio (CP) (%)'][years_list[i]]
            fundamentals.earnings_retention_ratio_percent = self.ratios['Earnings Retention Ratio (%)'][years_list[i]]
            fundamentals.cach_earnings_retention_ratio_percent = self.ratios['Cash Earnings Retention Ratio (%)'][years_list[i]]
            fundamentals.enterprice_value_cr = self.ratios['Enterprise Value (Cr.)'][years_list[i]]
            fundamentals.ev_over_net_operating_revenue_x = self.ratios['EV/Net Operating Revenue (X)'][years_list[i]]
            fundamentals.ev_over_ebitda_x = self.ratios['EV/EBITDA (X)'][years_list[i]]
            fundamentals.marketcap_over_net_operating_revenue_x = self.ratios['MarketCap/Net Operating Revenue (X)'][years_list[i]]
            fundamentals.retention_ratios_percent = self.ratios['Retention Ratios (%)'][years_list[i]]
            fundamentals.price_over_book_x = self.ratios['Price/BV (X)'][years_list[i]]
            fundamentals.price_over_net_operating_revenue_x = self.ratios['Price/Net Operating Revenue'][years_list[i]]
            fundamentals.earnings_yield = self.ratios['Earnings Yield'][years_list[i]]
            fundamentals.save()

