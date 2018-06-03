from .models import StockAsset, StockOrder
import openpyxl


class JuggernautHelper:

    def __init__(self):
        pass

    @staticmethod
    def extract_trades(file_handle):
        column_names = ('B', 'E', 'F', 'G', 'H', 'I', 'J')
        work_book = openpyxl.load_workbook(file_handle)
        sheet = work_book.get_sheet_by_name('TRADEBOOK')
        new_stock_order = StockOrder()
        for row in range(13, sheet.max_row + 1):
            stock_order_list = []
            for column in column_names:
                stock_order_list.append(sheet[column + str(row)].value)
            new_stock_order.prepare_stock_order_from_list(stock_order_list)
            if not StockAsset.objects.filter(stock_name__exact=new_stock_order.order_name).exists():
                new_symbol = StockAsset(stock_name=new_stock_order.order_name)
                new_symbol.save()
            if not StockOrder.objects.filter(order_name=new_stock_order.order_name,
                                             order_no=new_stock_order.order_no,
                                             order_trade_no=new_stock_order.order_trade_no
                                             ).exists():
                new_stock_order.save()

    @staticmethod
    def populate_profit_loss():
        for each_symbol in StockAsset.objects.all():
            all_orders = StockOrder.objects.filter(order_name__exact=each_symbol.stock_name).order_by('order_date')
            held_quantity = 0
            last_buy_price = 0
            last_sell_price = 0
            profit_loss = 0
            avg_sell_price = 0
            avg_buy_price = 0
            closed_value = 0
            closed_quantity = 0
            for order in all_orders:
                if order.order_type == 'B':
                    if held_quantity > 0:
                        avg_buy_price = ((avg_buy_price * held_quantity) + (order.order_rate * order.order_quantity))\
                        /(held_quantity + order.order_quantity)
                        avg_sell_price = 0
                        held_quantity = held_quantity + order.order_quantity
                        last_buy_price = order.order_rate
                    elif held_quantity < 0:
                        difference_quantity = abs(held_quantity) - order.order_quantity
                        if difference_quantity > 0:
                            profit_loss = profit_loss + (order.order_quantity * (avg_sell_price - order.order_rate))
                            avg_buy_price = 0
                            last_buy_price = order.order_rate
                            closed_quantity = closed_quantity + order.order_quantity
                            closed_value = closed_value + (order.order_quantity * order.order_rate)
                            held_quantity = 0 - difference_quantity
                        elif difference_quantity < 0:
                            profit_loss = profit_loss + (abs(held_quantity) * (avg_sell_price - order.order_rate))
                            avg_sell_price = 0
                            avg_buy_price = order.order_rate
                            last_buy_price = order.order_rate
                            closed_quantity = closed_quantity + abs(held_quantity)
                            closed_value = closed_value + (abs(held_quantity) * order.order_rate)
                            held_quantity = abs(difference_quantity)
                        else:
                            profit_loss = profit_loss + (abs(held_quantity) * (avg_sell_price - order.order_rate))
                            avg_buy_price = 0
                            avg_sell_price = 0
                            closed_quantity = closed_quantity + abs(held_quantity)
                            closed_value = closed_value + (abs(held_quantity) * order.order_rate)
                            held_quantity = difference_quantity
                    else:
                        avg_buy_price = order.order_rate
                        avg_sell_price = 0
                        last_buy_price = order.order_rate
                        held_quantity = order.order_quantity
                else:
                    if held_quantity > 0:
                        difference_quantity = held_quantity - order.order_quantity
                        if difference_quantity > 0:
                            profit_loss = profit_loss + (order.order_quantity * (order.order_rate - avg_buy_price))
                            avg_sell_price = 0
                            last_sell_price = order.order_rate
                            closed_quantity = closed_quantity + order.order_quantity
                            closed_value = closed_value + (order.order_quantity * avg_buy_price)
                            held_quantity = difference_quantity
                        elif difference_quantity < 0:
                            profit_loss = profit_loss + (held_quantity * (order.order_rate - avg_buy_price))
                            closed_quantity = closed_quantity + held_quantity
                            closed_value = closed_value + (held_quantity * avg_buy_price)
                            avg_buy_price = 0
                            avg_sell_price = order.order_rate
                            last_sell_price = order.order_rate
                            held_quantity = difference_quantity
                        else:
                            profit_loss = profit_loss + (held_quantity * (order.order_rate - avg_buy_price))
                            closed_quantity = closed_quantity + held_quantity
                            closed_value = closed_value + (held_quantity * avg_buy_price)
                            avg_buy_price = 0
                            avg_sell_price = 0
                            held_quantity = difference_quantity
                    elif held_quantity < 0:
                        avg_sell_price = ((avg_sell_price * abs(held_quantity)) + (order.order_rate * order.order_quantity))\
                        /(abs(held_quantity) + order.order_quantity)
                        avg_buy_price = 0
                        held_quantity = held_quantity - order.order_quantity
                        last_sell_price = order.order_rate
                    else:
                        avg_sell_price = order.order_rate
                        avg_buy_price = 0
                        last_sell_price = order.order_rate
                        held_quantity = 0 - order.order_quantity
            each_symbol.stock_avg_bought = avg_buy_price
            each_symbol.stock_avg_sell = avg_sell_price
            each_symbol.stock_last_sell = last_sell_price
            each_symbol.stock_last_buy = last_buy_price
            each_symbol.stock_units_closed = closed_quantity
            each_symbol.stock_units_held = held_quantity
            each_symbol.stock_closed_value = closed_value
            each_symbol.stock_current_value = abs(each_symbol.stock_units_held) * \
                                              (each_symbol.stock_avg_bought + each_symbol.stock_avg_sell)
            each_symbol.stock_profit_loss = profit_loss
            if closed_value:
                each_symbol.stock_pl_percent = (each_symbol.stock_profit_loss/closed_value) * 100
            else:
                each_symbol.stock_pl_percent = 0
            each_symbol.save()
