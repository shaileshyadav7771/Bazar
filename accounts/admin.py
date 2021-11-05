from django.contrib import admin
from .models import Accounts

from import_export.admin import ImportExportModelAdmin
# Register your models here.


class AccountsAdmin(ImportExportModelAdmin):
	list_display=['id','first_name','last_name','username','email','contact_number','date_joined','date_logined','is_active']
	###Adding this line so that we Can Search/filter user result in case of any changes or to Check last time when he updated#######
	search_fields = ('id','first_name','last_name','username','email','contact_number','date_joined','date_logined')
	readonly_fields = ('password',)  # for password read only in admin
	list_display_links = ('email', 'first_name', 'last_name')
	ordering = ('-date_joined',)

admin.site.register(Accounts,AccountsAdmin)

