from django.conf.urls import url
from .views import MawMainPage

urlpatterns = [
    url('', MawMainPage.as_view()),
]