from django.contrib import admin
from thanos.models import *


# Register your models here.
admin.site.register(Fundamental)
admin.site.register(Symbol)
admin.site.register(Sector)
admin.site.register(BalanceSheet)
admin.site.register(ProfitAndLossStatement)
admin.site.register(CashFlowStatement)
