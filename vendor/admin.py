from django.contrib import admin
from . import models

class AdminAccount(admin.ModelAdmin):
    list_display = ('id', 'balance')

class AdminVendor(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'address', 'created_at')

class AdminProduct(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'vendor', 'created_at')

class AdminTransaction(admin.ModelAdmin):
    list_display = ('id', 'invoice_number', 'total_amount', 'created_at')

# Register your models here.
admin.site.register(models.Account, AdminAccount)
admin.site.register(models.Vendor, AdminVendor)
admin.site.register(models.Product, AdminProduct)
admin.site.register(models.Transaction, AdminTransaction)