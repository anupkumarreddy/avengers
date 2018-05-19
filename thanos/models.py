from __future__ import unicode_literals

from django.db import models


class Symbols (models.Model):
    """Model to store known symbols"""

    MARKETS = ( ('NSE', 'NSE MARKET'), ('BSE', 'BSE MARKET'),  ('NFO', 'NFO_MARKET'))

    symbol_name = models.CharField(max_length=50)
    market_name = models.CharField(max_length=50, choices=MARKETS)

    def __str__(self):
        return self.symbol_name


class Fundamentals (models.Model):
    """Model to store all fundamental data for a symbol per year"""

    symbol = models.ForeignKey(Symbols, on_delete=models.CASCADE)
    year = models.DateField(null=True, blank=True)

    # Per share ratios
    basic_eps_rs = models.FloatField(null=True, blank=True)
    diluted_eps_rs = models.FloatField(null=True, blank=True)
    cash_eps_in_rs = models.FloatField(null=True, blank=True)
    book_value_exc_reserve_rs = models.FloatField(null=True, blank=True)
    book_value_inc_reserve_rs = models.FloatField(null=True, blank=True)
    dividend_rs = models.FloatField(null=True, blank=True)
    revenue_from_operations_rs = models.FloatField(null=True, blank=True)
    pbdit_rs = models.FloatField(null=True, blank=True)
    pbit_rs = models.FloatField(null=True, blank=True)
    pbt_rs = models.FloatField(null=True, blank=True)
    net_profit_rs = models.FloatField(null=True, blank=True)

    # Profitability Ratios
    pbdit_margin_percent = models.FloatField(null=True, blank=True)
    pbit_margin_percent = models.FloatField(null=True, blank=True)
    pbt_margin_percent = models.FloatField(null=True, blank=True)
    net_profit_margin_percent = models.FloatField(null=True, blank=True)
    return_on_networth_percent = models.FloatField(null=True, blank=True)
    return_on_capital_employed_percent = models.FloatField(null=True, blank=True)
    return_on_assets_percent = models.FloatField(null=True, blank=True)
    total_dept_to_equity_x = models.FloatField(null=True, blank=True)
    asset_turnover_ratio_percent = models.FloatField(null=True, blank=True)

    # Liquidity ratios
    current_ratio_x = models.FloatField(null=True, blank=True)
    quick_ratio_x = models.FloatField(null=True, blank=True)
    inventory_turnover_ratio_x = models.FloatField(null=True, blank=True)
    dividend_payout_ratio_cp_percent = models.FloatField(null=True, blank=True)
    dividend_payout_ratio_np_percent = models.FloatField(null=True, blank=True)
    earnings_retention_ratio_percent = models.FloatField(null=True, blank=True)
    cach_earnings_retention_ratio_percent = models.FloatField(null=True, blank=True)

    # Valuations Ratios
    enterprice_value_cr = models.FloatField(null=True, blank=True)
    ev_over_net_operating_revenue_x = models.FloatField(null=True, blank=True)
    ev_over_ebitda_x = models.FloatField(null=True, blank=True)
    marketcap_over_net_operating_revenue_x = models.FloatField(null=True, blank=True)
    retention_ratios_percent = models.FloatField(null=True, blank=True)
    price_over_book_x = models.FloatField(null=True, blank=True)
    price_over_net_operating_revenue_x = models.FloatField(null=True, blank=True)
    earnings_yield = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.symbol.symbol_name + self.year.strftime("%Y")

