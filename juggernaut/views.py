from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from models import StockAsset, StockOrder
from utils import JuggernautHelper
from django.db.models import Sum


class JuggernautMainPage (TemplateView):
    template_name = 'juggernaut/index.html'

    def get(self, request):
        data = {}
        data['assets'] = StockAsset.objects.all()
        data['total_profit_loss'] = StockAsset.objects.aggregate(Sum('stock_profit_loss'))['stock_profit_loss__sum']
        data['total_orders'] = StockOrder.objects.count()
        data['total_symbols'] = StockAsset.objects.count()
        juggernaut = loader.get_template(self.template_name)
        return HttpResponse(juggernaut.render({'data': data}, request))

    def post(self, request):
        data = {}
        if request.method == 'POST' and request.FILES['myfile']:
            file_handle = request.FILES['myfile']
            data['name'] = file_handle.name
            JuggernautHelper.extract_trades(file_handle)
            JuggernautHelper.populate_profit_loss()
        data['assets'] = StockAsset.objects.all()
        data['total_profit_loss'] = StockAsset.objects.aggregate(Sum('stock_profit_loss'))['stock_profit_loss__sum']
        data['total_orders'] = StockOrder.objects.count()
        data['total_symbols'] = StockAsset.objects.count()
        juggernaut = loader.get_template(self.template_name)
        return HttpResponse(juggernaut.render({'data': data}, request))
