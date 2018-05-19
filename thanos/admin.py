from django.contrib import admin
from thanos.models import Fundamentals, Symbols


# Register your models here.
admin.site.register(Fundamentals)
admin.site.register(Symbols)