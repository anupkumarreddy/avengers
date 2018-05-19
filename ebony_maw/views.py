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

    def __init__(self, url="", silent=True):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
        logger.disabled = silent
        if url == "":
            logging.warning("URL is not set properly")
        else:
            self.url = url
            logging.info("URL is set as %s ", url)

    def __prepare_soup(self):
        if self.__is_url_present():
            self.my_soup = soup(urllib.urlopen(self.url), "html.parser")
        else:
            logging.error("Cannot process fundamentals as URL is not set")

    def __is_url_present(self):
        return self.url != ""

    def extract_fundamentals(self):
        self.__prepare_soup()
        table = self.my_soup.find_all('table', {'class': 'table4'})[2]
        for index, tr in enumerate(table.find_all('tr')):
            td = tr.find_all('td')
            if len(td) == 6 and td[0].get_text() != "" and td[1].get_text() != "" and td[2].get_text() != "" and td[3].get_text() != "" and td[4].get_text() != "" and td[5].get_text() != "":
                logging.info("  Extracting %s: (%s, %s, %s, %s, %s) ... ", td[0].get_text(), td[1].get_text(), td[2].get_text(),
                             td[3].get_text(), td[4].get_text(), td[5].get_text())
                self.ratios[td[0].get_text()] = {'2017' : td[1].get_text(), '2016' : td[2].get_text(), '2015' : td[3].get_text(), '2014' : td[4].get_text(), '2013' : td[5].get_text()}

    def push_to_database(self):
        years_list = ['2017', '2016', '2015', '2014', '2013']
        symbol_name = "NOCIL"
        symbol = Symbols()
        symbol.symbol_name = symbol_name
        symbol.save()
        for i in range(5):
            fundamentals = Fundamentals()
            fundamentals.symbol = symbol
            fundamentals.year = datetime.strptime(years_list[i]+' 01 01', '%Y %m %d')
            fundamentals.basic_eps_rs = self.ratios['Basic EPS (Rs.)'][years_list[i]]
            logging.info("Basic EPS value is %d", fundamentals.basic_eps_rs)
            fundamentals.save()
            # fundamentals.diluted_eps_rs =
            # fundamentals.cash_eps_in_rs =
            # fundamentals.book_value_exc_reserve_rs =
            # fundamentals.book_value_inc_reserve_rs =
            # fundamentals.dividend_rs =
            # fundamentals.revenue_from_operations_rs =
            # fundamentals.pbdit_rs =
            # fundamentals.pbit_rs =
            # fundamentals.pbt_rs =
            # fundamentals.net_profit_rs =
            #
            # fundamentals.pbdit_margin_percent =
            # fundamentals.pbit_margin_percent =
            # fundamentals.pbt_margin_percent =
            # fundamentals.net_profit_margin_percent =
            # fundamentals.return_on_networth_percent =
            # fundamentals.return_on_capital_employed_percent =
            # fundamentals.return_on_assets_percent =
            # fundamentals.total_dept_to_equity_x =
            # fundamentals.asset_turnover_ratio_percent =
            #
            # fundamentals.current_ratio_x =
            # fundamentals.quick_ratio_x =
            # fundamentals.inventory_turnover_ratio_x =
            # fundamentals.dividend_payout_ratio_cp_percent =
            # fundamentals.dividend_payout_ratio_np_percent =
            # fundamentals.earnings_retention_ratio_percent =
            # fundamentals.cach_earnings_retention_ratio_percent =
            #
            # fundamentals.enterprice_value_cr =
            # fundamentals.ev_over_net_operating_revenue_x =
            # fundamentals.ev_over_ebitda_x =
            # fundamentals.marketcap_over_net_operating_revenue_x =
            # fundamentals.retention_ratios_percent =
            # fundamentals.price_over_book_x =
            # fundamentals.price_over_net_operating_revenue_x =
            # fundamentals.earnings_yield =

