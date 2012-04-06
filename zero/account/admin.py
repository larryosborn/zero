from django.contrib import admin
from django.contrib.auth.models import User
from zero.account.models import Account, Asset, Transaction

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance',)

class AssetAdmin(admin.ModelAdmin):
    pass

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('company', 'quantity', 'price', 'date', 'user')
    pass

admin.site.register(Account, AccountAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Transaction, TransactionAdmin)