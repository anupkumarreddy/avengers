from __future__ import unicode_literals
from django.db import models
import datetime


class StockAsset (models.Model):

    stock_name = models.CharField(max_length=250)
    stock_avg_bought = models.FloatField(blank=True, null=True)
    stock_last_buy = models.FloatField(blank=True, null=True)
    stock_units_closed = models.IntegerField(blank=True, null=True)
    stock_units_held = models.IntegerField(blank=True, null=True)
    stock_avg_sell = models.FloatField(blank=True, null=True)
    stock_last_sell = models.FloatField(blank=True, null=True)
    stock_closed_value = models.FloatField(blank=True, null=True)
    stock_current_value = models.FloatField(blank=True, null=True)
    stock_profit_loss = models.FloatField(blank=True, null=True)
    stock_pl_percent = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.stock_name


class StockOrder (models.Model):

    order_date = models.DateField(blank=True, null=True)
    order_name = models.CharField(max_length=200)
    order_type = models.CharField(max_length=10)
    order_quantity = models.IntegerField(blank=True, null=True)
    order_rate = models.FloatField(blank=True, null=True)
    order_no = models.CharField(max_length=200)
    order_trade_no = models.CharField(max_length=200)

    def prepare_stock_order_from_list(self, stock_order_list):
        self.order_date = datetime.datetime.strptime(stock_order_list[0], '%d-%m-%Y').strftime('%Y-%m-%d')
        self.order_name = stock_order_list[1]
        self.order_type = stock_order_list[2]
        self.order_quantity = stock_order_list[3]
        self.order_rate = stock_order_list[4]
        self.order_no = stock_order_list[5]
        self.order_trade_no = stock_order_list[6]

    def __str__(self):
        return self.order_name
