from django.contrib import admin
from zero.company.models import Company, Price
from django.contrib.auth.models import User

class CompanyAdmin(admin.ModelAdmin):
    fields = ('symbol', 'name', 'exchange','sector','location')
    list_filter = ('exchange','sector')
    list_display = ('symbol', 'name', 'exchange','sector','location')
    #list_display_links = ('name', 'symbol', 'exchange')

class PriceAdmin(admin.ModelAdmin):
    fields = ('company', 'category', 'date','opened', 'low','high','closed','volume','adj_closed')
    list_filter = ('company', 'category', 'date')
    list_display = ('company', 'category', 'date','opened', 'low','high','closed','volume','adj_closed')

admin.site.register(Company, CompanyAdmin)
admin.site.register(Price, PriceAdmin)