from django.contrib import admin
from .models import EmployerProfile

# Register your models here.

#admin.site.register(EmployerProfile)


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
	list_display = [
	'company_name',
	'contact_email',
	'is_member',
	]    

	list_filter = [
	'is_member',
	]

	search_fields = [
	'company_name',
	'contact_email',
	'company_description',
	]