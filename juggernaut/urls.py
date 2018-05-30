from django.conf.urls import url
from .views import JuggernautMainPage

urlpatterns = [
    url('', JuggernautMainPage.as_view(template_name='juggernaut/index.html'), name='juggernaut_index'),
]