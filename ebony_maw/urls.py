from django.conf.urls import url
from .views import MawMainPage

urlpatterns = [
    url('symbol/([0-9]+)', MawMainPage.as_view(template_name='maw/dashboard.html'), name='dashboard'),
]