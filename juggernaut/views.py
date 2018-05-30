from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader
from .models import StockAsset, StockOrder
import openpyxl
import datetime


class JuggernautMainPage (TemplateView):
    template_name = 'juggernaut/index.html'

    def get(self, request):
        data = {}
        data['assets'] = StockAsset.objects.all()
        juggernaut = loader.get_template(self.template_name)
        return HttpResponse(juggernaut.render({'data': data}, request))

    def post(self, request):
        data = {}
        all_symbols = StockAsset.objects.all()
        all_orders = StockOrder.objects.all()
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            data['name'] = myfile.name
            wb = openpyxl.load_workbook(myfile)
            sheet = wb.get_sheet_by_name('TRADEBOOK')
            print('Reading rows...')
            for row in range(13, sheet.max_row + 1):
                date = sheet['B' + str(row)].value
                new_date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
                print new_date
                time = sheet['C' + str(row)].value
                symbol = sheet['E' + str(row)].value
                order_type = sheet['F' + str(row)].value
                qty = sheet['G' + str(row)].value
                rate = sheet['H' + str(row)].value
                order_no = sheet['I' + str(row)].value
                trade_no = sheet['J' + str(row)].value
                if not all_symbols.filter(stock_name__exact=symbol).exists():
                    new_symbol = StockAsset(stock_name=symbol)
                    new_symbol.save()
                if not all_orders.filter(order_name=symbol, order_no=order_no, order_trade_no=trade_no).exists():
                    new_order = StockOrder(order_date=new_date, order_name=symbol, order_type=order_type, order_quantity=qty,
                                       order_rate=rate, order_no=order_no, order_trade_no=trade_no)
                    new_order.save()
                print symbol, order_type, qty, rate
            for each_symbol in StockAsset.objects.all():
                total_sell_quantity = 0
                total_buy_quantity = 0
                total_sell_price = 0
                total_buy_price = 0
                last_sell_price = 0
                last_buy_price = 0
                total_buy_trades = 0
                total_sell_trades = 0
                for each_order in StockOrder.objects.filter(order_name=each_symbol.stock_name):
                    if each_order.order_type == 'B':
                        total_buy_price = total_buy_price + each_order.order_rate
                        total_buy_quantity = total_buy_quantity + each_order.order_quantity
                        total_buy_trades = total_buy_trades + 1
                        last_buy_price = each_order.order_rate
                        #print "BUY:", each_symbol.stock_name, total_buy_price, total_buy_quantity
                    else :
                        total_sell_price = total_sell_price + each_order.order_rate
                        total_sell_quantity = total_sell_quantity + each_order.order_quantity
                        last_sell_price = each_order.order_rate
                        total_sell_trades = total_sell_trades + 1
                        #print "SELL:", each_symbol.stock_name, total_sell_price, total_sell_quantity
                if total_buy_trades:
                    each_symbol.stock_avg_bought = total_buy_price/total_buy_trades
                else :
                    each_symbol.stock_avg_bought = 0
                each_symbol.stock_last_buy = last_buy_price
                if total_sell_trades:
                    each_symbol.stock_avg_sell = total_sell_price/total_sell_trades
                else:
                    each_symbol.stock_avg_sell = 0
                each_symbol.stock_last_sell = last_sell_price
                each_symbol.stock_units_closed = total_sell_quantity
                each_symbol.stock_units_held = total_buy_quantity-total_sell_quantity
                each_symbol.stock_closed_value = total_sell_quantity * each_symbol.stock_avg_bought
                each_symbol.stock_current_value = each_symbol.stock_units_held * each_symbol.stock_avg_bought
                each_symbol.stock_profit_loss = total_sell_quantity * (each_symbol.stock_avg_sell - each_symbol.stock_avg_bought)
                if each_symbol.stock_closed_value:
                    each_symbol.stock_pl_percent = (each_symbol.stock_profit_loss/each_symbol.stock_closed_value) * 100
                else :
                    each_symbol.stock_pl_percent = 0
                each_symbol.save()
        data['assets'] = StockAsset.objects.all()
        juggernaut = loader.get_template(self.template_name)

        return HttpResponse(juggernaut.render({'data': data}, request))
