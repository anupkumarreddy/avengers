from __future__ import unicode_literals

from django.db import models


class Sector (models.Model):
    """All sectorial information is stored here"""

    sector_name = models.CharField(max_length=100)

    def __str__(self):
        return self.sector_name


class Symbol (models.Model):
    """Model to store known symbols"""

    MARKETS = ( ('NSE', 'NSE MARKET'), ('BSE', 'BSE MARKET'),  ('NFO', 'NFO_MARKET'))

    symbol_name = models.CharField(max_length=50)
    market_name = models.CharField(max_length=50, choices=MARKETS)
    symbol_sector_name = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, blank=True)
    symbol_url = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.symbol_name


class Fundamental (models.Model):
    """Model to store all fundamental data for a symbol per year"""

    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
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


class BalanceSheet (models.Model):

    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    sheet_year = models.DateField(null=True, blank=True)

    equity_share_capital = models.FloatField(null=True, blank=True)
    reserves_and_surples = models.FloatField(null=True, blank=True)
    total_share_holders_fund = models.FloatField(null=True, blank=True)

    long_term_borrowings = models.FloatField(null=True, blank=True)
    deferred_tax_liabilities_net = models.FloatField(null=True, blank=True)
    long_term_provisions = models.FloatField(null=True, blank=True)
    total_non_current_liabilities = models.FloatField(null=True, blank=True)

    short_term_borrowings = models.FloatField(null=True, blank=True)
    trade_payables = models.FloatField(null=True, blank=True)
    other_current_liabilities = models.FloatField(null=True, blank=True)
    short_term_provisions = models.FloatField(null=True, blank=True)
    total_current_libilities = models.FloatField(null=True, blank=True)
    total_capital_and_liabilities = models.FloatField(null=True, blank=True)

    tangible_assets = models.FloatField(null=True, blank=True)
    intangible_assets = models.FloatField(null=True, blank=True)
    capital_work_in_progress = models.FloatField(null=True, blank=True)
    fixed_assets = models.FloatField(null=True, blank=True)

    non_current_investments = models.FloatField(null=True, blank=True)
    long_term_loans_and_advances = models.FloatField(null=True, blank=True)
    total_non_current_assets = models.FloatField(null=True, blank=True)

    inventories = models.FloatField(null=True, blank=True)
    trade_receivables = models.FloatField(null=True, blank=True)
    cash_and_cach_equivalents = models.FloatField(null=True, blank=True)
    short_term_loans_and_advances = models.FloatField(null=True, blank=True)
    other_current_assets = models.FloatField(null=True, blank=True)
    total_current_assets = models.FloatField(null=True, blank=True)
    total_assets = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.symbol.symbol_name + self.sheet_year.strftime("%Y")


class ProfitAndLossStatement (models.Model):

    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    sheet_year = models.DateField(null=True, blank=True)

    revenue_from_operation_gross = models.FloatField(null=True, blank=True)
    excise_service_tax = models.FloatField(null=True, blank=True)
    revenue_from_operations = models.FloatField(null=True, blank=True)
    other_operating_revenue = models.FloatField(null=True, blank=True)
    total_operating_revenue = models.FloatField(null=True, blank=True)
    other_income = models.FloatField(null=True, blank=True)
    total_revenue = models.FloatField(null=True, blank=True)

    cost_of_materials_consumed = models.FloatField(null=True, blank=True)
    purchase_of_stock_in_trade = models.FloatField(null=True, blank=True)
    changes_in_inventories = models.FloatField(null=True, blank=True)
    employee_benefit_expenses = models.FloatField(null=True, blank=True)
    finance_cost = models.FloatField(null=True, blank=True)
    depreciation_and_amortisation_expenses = models.FloatField(null=True, blank=True)
    other_expenses = models.FloatField(null=True, blank=True)
    total_expenses = models.FloatField(null=True, blank=True)

    profit_loss_before_extraordinary_items = models.FloatField(null=True, blank=True)
    exceptional_items = models.FloatField(null=True, blank=True)
    profit_loss_before_tax = models.FloatField(null=True, blank=True)
    current_tax = models.FloatField(null=True, blank=True)
    deferred_tax = models.FloatField(null=True, blank=True)
    tax_for_earliar_years = models.FloatField(null=True, blank=True)
    total_tax_expense = models.FloatField(null=True, blank=True)
    profit_loss_after_tax_before_extraordinary_items = models.FloatField(null=True, blank=True)
    profit_loss_from_continuing_operations = models.FloatField(null=True, blank=True)
    profit_loss_for_the_period = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.symbol.symbol_name + self.sheet_year.strftime("%Y")


class CashFlowStatement (models.Model):

    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    sheet_year = models.DateField(null=True, blank=True)

    net_profit_loss_before_extraordinary_and_tax = models.FloatField(null=True, blank=True)
    net_cash_flow_from_operating_activities = models.FloatField(null=True, blank=True)
    net_cash_used_in_investing_activities = models.FloatField(null=True, blank=True)
    net_cash_used_from_financing_activities = models.FloatField(null=True, blank=True)
    foreign_exchange_gains_losses = models.FloatField(null=True, blank=True)
    net_inc_dec_cash_and_cash_equivalents = models.FloatField(null=True, blank=True)
    cash_and_cash_equivalents_begin_of_year = models.FloatField(null=True, blank=True)
    cash_and_cash_equivalents_end_of_year = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.symbol.symbol_name + self.sheet_year.strftime("%Y")
