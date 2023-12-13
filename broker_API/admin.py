from django.contrib import admin

from .models import Stock, Portfolio, Investor, Admin

admin.site.register(Investor)
admin.site.register(Admin)
admin.site.register(Stock)
admin.site.register(Portfolio)
