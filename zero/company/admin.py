from django.contrib import admin
from zero.company.models import Company, Price, Index, IndexCompany
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

class IndexAdmin(admin.ModelAdmin):
    fields = ('name',)

class IndexCompanyAdmin(admin.ModelAdmin):
    fields = ('index','company',)
    list_filter = ('index',)
    list_display = ('index', 'company')

admin.site.register(Company, CompanyAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(IndexCompany, IndexCompanyAdmin)