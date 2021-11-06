from django.contrib import admin
from .models import Product

from import_export.admin import ImportExportModelAdmin
# Register your models here.


class ProductAdmin(ImportExportModelAdmin):
	list_display=['id','product_name','price','images','stock','is_available','category','created_date','modified_date','description']
	###Adding this line so that we Can Search/filter user result in case of any changes or to Check last time when he updated#######
	search_fields = ('id','product_name','price','images','stock','is_available','category','created_date','modified_date','description')
	list_display_links = ('id','product_name','price','images','stock',)
	ordering = ('-price',)
	prepopulated_fields = {"slug": ('product_name',)}

admin.site.register(Product,ProductAdmin)
