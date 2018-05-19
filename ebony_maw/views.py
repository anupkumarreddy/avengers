from django.shortcuts import render
from django.http import HttpResponse
from thanos.models import Fundamentals
from django.template import loader
from django.views.generic import TemplateView
from bs4 import BeautifulSoup as soup
import logging
import urllib


class MawMainPage (TemplateView):
    template_name = 'maw/maw.html'

    def post(self, request, *args, **kwargs):
        url = request.POST['url']
        fundamentals = Fundamentals(url, silent=False)
        fundamentals.extract_fundamentals()
        data = "Extraction done..."
        maw = loader.get_template(self.template_name)
        return HttpResponse(maw.render({'url': data}, request))


class Fundamentals:
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

# def index(request):
#     url = ""
#     if request.method=='POST':
#         url = request.POST['url']
#     maw = loader.get_template('maw/maw.html')
#     context = {'url': url, }
#     return HttpResponse(maw.render(context, request))