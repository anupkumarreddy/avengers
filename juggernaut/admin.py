from django.contrib import admin
from .models import StockAsset, StockOrder


admin.site.register(StockAsset)
admin.site.register(StockOrder)