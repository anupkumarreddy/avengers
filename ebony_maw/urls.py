from django.conf.urls import url
from .views import MawMainPage

urlpatterns = [
    # url('all_symbols/', MawMainPage.as_view(template_name='maw/all_symbol.html'), name='all_symbols'),
    # url('symbol/', MawMainPage.as_view(template_name='maw/symbol.html'), name='symbol'),
    url('', MawMainPage.as_view(template_name='maw/dashboard.html'), name='dashboard'),
]