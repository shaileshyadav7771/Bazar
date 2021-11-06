from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category
# Register your models here.

class CategoryAdmin(ImportExportModelAdmin):
	list_display=['id','category_name','slug','description','cat_image']
	###Adding this line so that we Can Search/filter user result in case of any changes or to Check last time when he updated#######
	search_fields = ('category_name','slug','description','cat_image')
	prepopulated_fields = {"slug":('category_name',)}


admin.site.register(Category,CategoryAdmin)
