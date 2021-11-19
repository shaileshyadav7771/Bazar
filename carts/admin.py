from django.contrib import admin
from .models import Cart,CartItem
from import_export.admin import ImportExportModelAdmin
# Register your models here.



class CartAdmin(ImportExportModelAdmin):
	list_display=['Cart_id','date_added']
admin.site.register(Cart, CartAdmin)



class CartItemAdmin(ImportExportModelAdmin):
	list_display = ['product','cart','quantity','is_active']
admin.site.register(CartItem,CartItemAdmin)

